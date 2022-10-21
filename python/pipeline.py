class Pipeline:
    def __init__(self, config, emailer, log):
        self.config = config
        self.emailer = emailer
        self.log = log

    def run(self, project):
        tests_passed = False
        deploy_successful = False

        tests_passed = self.run_tests(project, tests_passed)
        deploy_successful = self.deploy_project(deploy_successful, project, tests_passed)
        email_summary = self.create_email_summary(deploy_successful, tests_passed)
        self.send_email_summary(email_summary)

    def send_email_summary(self, email_summary):
        if self.config.send_email_summary():
            self.log.info("Sending email")
            self.emailer.send(email_summary)
        else:
            self.log.info("Email disabled")

    def create_email_summary(self, deploy_successful, tests_passed):
        if tests_passed:
            if deploy_successful:
                email_summary = "Deployment completed successfully"
            else:
                email_summary = "Deployment failed"
        else:
            email_summary = "Tests failed"
        return email_summary

    def deploy_project(self, deploy_successful, project, tests_passed):
        if tests_passed:
            if "success" == project.deploy():
                self.log.info("Deployment successful")
                deploy_successful = True
            else:
                self.log.error("Deployment failed")
        return deploy_successful

    def run_tests(self, project, tests_passed):
        if project.has_tests():
            if "success" == project.run_tests():
                self.log.info("Tests passed")
                tests_passed = True
            else:
                self.log.error("Tests failed")
        else:
            self.log.info("No tests")
            tests_passed = True
        return tests_passed
