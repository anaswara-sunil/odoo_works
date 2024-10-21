/** @odoo-module */
import { _t } from "@web/core/l10n/translation";
import { PaymentInterface } from "@point_of_sale/app/payment/payment_interface";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { sprintf } from "@web/core/utils/strings";
const { DateTime } = luxon;

export class PaymentMoneris extends PaymentInterface {
    setup() {
        super.setup(...arguments);
        console.log(this,'this')
        this.paymentLineResolvers = {};
    }

    send_payment_request(cid) {
        console.log(cid,'cid')
        super.send_payment_request(cid);
        return this._moneris_pay(cid);
    }

    pending_moneris_line() {
        return this.pos.getPendingPaymentLine("moneris");
    }

    set_most_recent_service_id(id) {
       this.most_recent_service_id = id;
    }

    _handle_odoo_connection_failure(data = {}) {
        // handle timeout
        var line = this.pending_moneris_line();
        if (line) {
            line.set_payment_status("retry");
        }
        this._show_error(
            _t(
                "Could not connect to the Odoo server, please check your internet connection and try again."
            )
        );

        return Promise.reject(data); // prevent subsequent onFullFilled's from being called
    }

    _call_moneris(data, operation = false) {
        console.log('_call_moneris')
        return this.env.services.orm.silent
            .call("pos.payment.method", "proxy_moneris_request", [
                [this.payment_method.id],
                data,
                operation,
            ])
            .catch(this._handle_odoo_connection_failure.bind(this));
    }

    _moneris_get_sale_id() {
    var config = this.pos.config;
    return sprintf("%s (ID: %s)", config.display_name, config.id);
    }

    _moneris_common_message_header() {
        var config = this.pos.config;
        this.most_recent_service_id = Math.floor(Math.random() * Math.pow(2, 64)).toString(); // random ID to identify request/response pairs
        this.most_recent_service_id = this.most_recent_service_id.substring(0, 10); // max length is 10

        return {
            ProtocolVersion: "3.0",
            MessageClass: "Service",
            MessageType: "Request",
            SaleID: this._moneris_get_sale_id(config),
            ServiceID: this.most_recent_service_id,
            POIID: this.payment_method.moneris_terminal_identifier,
        };
    }

    _moneris_pay_data() {
        var order = this.pos.get_order();
        var config = this.pos.config;
        var line = order.selected_paymentline;
        var data = {
            SaleToPOIRequest: {
                MessageHeader: Object.assign(this._moneris_common_message_header(), {
                    MessageCategory: "Payment",
                }),
                PaymentRequest: {
                    SaleData: {
                        SaleTransactionID: {
                            TransactionID: `${order.uid}--${order.pos_session_id}`,
                            TimeStamp: DateTime.now().toFormat("yyyy-MM-dd'T'HH:mm:ssZZ"), // iso format: '2018-01-10T11:30:15+00:00'
                        },
                    },
                    PaymentTransaction: {
                        AmountsReq: {
                            Currency: this.pos.currency.name,
                            RequestedAmount: line.amount,
                        },
                    },
                },
            },
        };

//        if (config.adyen_ask_customer_for_tip) {
//            data.SaleToPOIRequest.PaymentRequest.SaleData.SaleToAcquirerData =
//                "tenderOption=AskGratuity";
//        }
        console.log(data,'_moneris_pay_data')
        return data;
    }

    _moneris_pay(cid) {
        var order = this.pos.get_order();
        console.log(order,'order')
        if (order.selected_paymentline.amount < 0) {
            this._show_error(_t("Cannot process transactions with negative amount."));
            return Promise.resolve();
        }

        var data = this._moneris_pay_data();
        var line = order.paymentlines.find((paymentLine) => paymentLine.cid === cid);
        line.setTerminalServiceId(this.most_recent_service_id);
        return this._call_moneris(data).then((data) => {
            return this._moneris_handle_response(data);
        });
    }

    _moneris_handle_response(response) {
        var line = this.pending_moneris_line();

        if (response.error && response.error.status_code == 401) {
            this._show_error(_t("Authentication failed. Please check your Moneris credentials."));
            line.set_payment_status("force_done");
            return false;
        }

        response = response.SaleToPOIRequest;
        if (response?.EventNotification?.EventToNotify === "Reject") {
            console.error("error from Moneris", response);

            var msg = "";
            if (response.EventNotification) {
                var params = new URLSearchParams(response.EventNotification.EventDetails);
                msg = params.get("message");
            }

            this._show_error(_t("An unexpected error occurred. Message from Moneris: %s", msg));
            if (line) {
                line.set_payment_status("force_done");
            }
            return false;
        } else {
            line.set_payment_status("waitingCard");
            return this.waitForPaymentConfirmation();
        }
    }

     _show_error(msg, title) {
        if (!title) {
            title = _t("Moneris Error");
        }
        this.env.services.popup.add(ErrorPopup, {
            title: title,
            body: msg,
        });
    }
}

