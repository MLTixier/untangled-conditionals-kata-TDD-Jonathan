class Pipeline:
    def __init__(self, config, emailer, log):
        self.config = config
        self.emailer = emailer
        self.log = log

    def run(self, project):
        if not project.has_tests():
            tests_passed = True
            self.log.info("No tests")
        else:
            tests_passed = self.run_tests(project)
        deploy_successful = self.deploy_project(project) if tests_passed else False


    def send_email_summary(self, email_summary):
        if self.config.send_email_summary():
            self.log.info("Sending email")
            self.emailer.send(email_summary)
        else:
            self.log.info("Email disabled")


    def deploy_project(self, project):
        if project.is_deploy_success():
            self.log.info("Deployment successful")
            self.send_email_summary("Deployment completed successfully")
        else:
            self.log.error("Deployment failed")
            self.send_email_summary("Deployment failed")
        return project.is_deploy_success()

    def run_tests(self, project):
        if project.is_run_tests_success():
            self.log.info("Tests passed")
        else:
            self.log.error("Tests failed")
            self.send_email_summary("Tests failed")
        return project.is_run_tests_success()
