/** @odoo-module **/
import SurveyFormWidget from '@survey/js/survey_form';

SurveyFormWidget.include({

     init() {
        this._super(...arguments);
        this.orm = this.bindService("orm");
    },
    async start(options) {
        this._super(...arguments);
//        const res = await this.orm.call("ir.config_parameter","get_param",['idle_time'])
//        this.quiz_idle_time = res;
        this.quiz_idle_time = 3;
        this.quiz_timeout_duration = 3;
        this.flag = false;

        this.idleTime = parseInt(this.quiz_idle_time) || 60;
        this.timeoutDuration = parseInt(this.quiz_timeout_duration) || 120;
        this.idleSeconds = this.idleTime;
        this.timeoutSeconds = this.timeoutDuration;
//        this.initIdleTimer();
    },

    _onSubmit: function (event) {
        this._super(...arguments)
        if (event.currentTarget.value === 'start') {
            this.initIdleTimer();
        }
    },
// Idle time from configuration
    async initIdleTimer() {
        var self = this;

        $(document).on('mousemove keydown',resetTimer);

        var interval = setInterval(async () => {
           self.idleSeconds--;
           self.flag = false;
           console.log(self.idleSeconds,'first-')
           $(document).on('mousemove keydown',resetTimer);
           if (self.idleSeconds == 0  ) {
               console.log('call for second',self.idleSeconds)
               clearInterval(interval);
               self.flag = true;
               self.idleSeconds = self.idleTime;
               await startTimeout();
              }
        }, 2000);

        function resetTimer() {
           console.log('RESET')
           self.timeoutSeconds = self.timeoutDuration;
           self.idleSeconds = self.idleTime;
           self.flag = false;
           document.querySelector('.o_survey_idle_timer').innerHTML = ""

        }

        function startTimeout(){
           var timerInterval = setInterval(async () =>{
               if (self.flag == true && self.idleSeconds ==self.idleTime){
                   self.timeoutSeconds--;
                   console.log(self.timeoutSeconds,'second-')
                   document.querySelector('.o_survey_idle_timer').innerHTML = self.timeoutSeconds + " " + "seconds left"
                   $(document).on('mousemove keydown',resetTimer);
                   if (self.timeoutSeconds == 0 && self.idleSeconds == 0) {
                      console.log('call for next page')
                      clearInterval(timerInterval);
                      document.querySelector('.o_survey_idle_timer').innerHTML = ""
                      self.timeoutSeconds = self.timeoutDuration;
                      self.idleSeconds = self.idleTime
                      await self.moveToNextPage();
                   }
               }
               else if (self.flag == false){
                  self.initIdleTimer();
               }
           }, 2000);
        }

     },

    moveToNextPage: function () {
        var nextButton = document.querySelector('button[type="submit"]');
        if (nextButton) {
            nextButton.click();
            this.initIdleTimer();
       }
    },

});