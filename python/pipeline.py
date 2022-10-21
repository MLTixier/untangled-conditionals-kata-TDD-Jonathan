class ExceptionTestsFailed(Exception):
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
            self.run_tests(project)
            self.deploy_project(project)
            self.send_email_summary("Deployment completed successfully")
        except ExceptionTestsFailed:
            self.send_email_summary("Tests failed")
        except ExceptionDeploymentFailed:
            self.send_email_summary("Deployment failed")

    def send_email_summary(self, summary):
        if self.config.send_email_summary():
            self.log.info("Sending email")
            self.emailer.send(summary)
        else:
            self.log.info("Email disabled")

    def deploy_project(self, project):
        if "success" != project.deploy():
            self.log.error("Deployment failed")
            raise ExceptionDeploymentFailed

        self.log.info("Deployment successful")

    def run_tests(self, project):
        if not project.has_tests():
            self.log.info("No tests")
            return

        if "success" != project.run_tests():
            self.log.error("Tests failed")
            raise ExceptionTestsFailed

        self.log.info("Tests passed")