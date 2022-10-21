class Pipeline:
    def __init__(self, config, emailer, log):
        self.config = config
        self.emailer = emailer
        self.log = log

    def run(self, project):
        tests_passed = False
        deploy_successful = False

        tests_passed = self.run_tests(project)
        deploy_successful = self.deploy_project(deploy_successful, project, tests_passed)
        summary = self.define_email_summary(deploy_successful, tests_passed)
        self.send_email_summary(summary)

    def send_email_summary(self, summary):
        if self.config.send_email_summary():
            self.log.info("Sending email")
            self.emailer.send(summary)
        else:
            self.log.info("Email disabled")

    def define_email_summary(self, deploy_successful, tests_passed):
        if tests_passed:
            if deploy_successful:
                summary = "Deployment completed successfully"
            else:
                summary = "Deployment failed"
        else:
            summary = "Tests failed"
        return summary

    def deploy_project(self, deploy_successful, project, tests_passed):
        if tests_passed:
            if "success" == project.deploy():
                self.log.info("Deployment successful")
                deploy_successful = True
            else:
                self.log.error("Deployment failed")
        return deploy_successful

    def run_tests(self, project):
        if not project.has_tests():
            self.log.info("No tests")
            return True

        if "success" != project.run_tests():
            self.log.error("Tests failed")
            return False

        self.log.info("Tests passed")
        return True
