class ExceptionTestsFailed (Exception):
    pass


class ExceptionDeploymentFailed(Exception):
    pass


class Pipeline:
    def __init__(self, config, emailer, log):
        self.config = config
        self.emailer = emailer
        self.log = log

    def run(self, project):
        try:
            if not project.has_tests():
                self.log.info("No tests")
                self.deploy_project(project)
            else:
                self.run_tests(project)
                if project.is_run_tests_success():
                    self.deploy_project(project)
        except ExceptionTestsFailed:
            self.send_email_summary("Tests failed")
        except ExceptionDeploymentFailed:
            self.send_email_summary("Deployment failed")

    def send_email_summary(self, email_summary):
        if self.config.send_email_summary():
            self.log.info("Sending email")
            self.emailer.send(email_summary)
        else:
            self.log.info("Email disabled")

    def deploy_project(self, project):
        if not project.is_deploy_success():
            self.log.error("Deployment failed")
            raise ExceptionDeploymentFailed()

        self.log.info("Deployment successful")
        self.send_email_summary("Deployment completed successfully")

    def run_tests(self, project):
        if not project.is_run_tests_success():
            self.log.error("Tests failed")
            raise ExceptionTestsFailed

        self.log.info("Tests passed")
