class Pipeline:
    def __init__(self, config, emailer, log):
        self.config = config
        self.emailer = emailer
        self.log = log

    def run_tests(self, project, tests_passed, deploy_successful):
        if project.has_tests():
            if "success" == project.run_tests():
                self.log.info("Tests passed")
                tests_passed = True
            else:
                self.log.error("Tests failed")
        else:
            self.log.info("No tests")
            tests_passed = True
        return tests_passed, deploy_successful

    def run(self, project):
        tests_passed = False
        deploy_successful = False

        tests_passed, deploy_successful = self.run_tests(project, tests_passed, deploy_successful)

        if tests_passed:
            if "success" == project.deploy():
                self.log.info("Deployment successful")
                deploy_successful = True
            else:
                self.log.error("Deployment failed")

        if self.config.send_email_summary():
            self.log.info("Sending email")
            if tests_passed:
                if deploy_successful:
                    self.emailer.send("Deployment completed successfully")
                else:
                    self.emailer.send("Deployment failed")
            else:
                self.emailer.send("Tests failed")
        else:
            self.log.info("Email disabled")
