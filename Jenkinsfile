pipeline {
    agent any

    environment {
        JMETER_HOME = 'C:\\JmeterInstallation\\apache-jmeter-5.6.3'   // ← your actual JMeter path
        TEST_PLAN   = 'altoro_test.jmx'
        RESULTS_JTL = 'results\\results.jtl'
        REPORT_DIR  = 'results\\html-report'
    }

    stages {

        stage('Clean Previous Results') {
            steps {
                bat 'if exist results rmdir /s /q results'
                bat 'mkdir results'
            }
        }

        stage('Run JMeter Test') {
            steps {
                bat """
                    "%JMETER_HOME%\\bin\\jmeter.bat" -n ^
                        -t "%TEST_PLAN%" ^
                        -l "%RESULTS_JTL%" ^
                        -e ^
                        -o "%REPORT_DIR%" ^
                        -Djmeter.save.saveservice.output_format=csv ^
                        -Djmeter.save.saveservice.success=true ^
                        -Djmeter.save.saveservice.response_code=true ^
                        -Djmeter.save.saveservice.label=true
                """
            }
        }

        stage('Performance Gate') {
            steps {
                perfReport(
                    sourceDataFiles:        'results\\results.jtl',
                    errorFailedThreshold:   2,
                    errorUnstableThreshold: 1,
                    compareBuildPrevious:   true
                )
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML([
                    allowMissing:          false,
                    alwaysLinkToLastBuild: true,
                    keepAll:               true,
                    reportDir:             'results\\html-report',
                    reportFiles:           'index.html',
                    reportName:            'JMeter Report'
                ])
            }
        }
    }

    post {
        success {
            echo 'BUILD PASSED — Error rate within threshold.'
        }
        failure {
            echo 'BUILD FAILED — Error rate exceeded 2% or test crashed.'
        }
    }
}