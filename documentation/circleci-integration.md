# CircleCI Integration

You can easily use CircleCI (https://circleci.com/) to build, test and push a Docker image to AWS ECR as part of a CI/CD pipeline.

## AWS ECR

Configure AWS CLI inside the development machine:

```ssh
aws configure
```

Create an AWS ECR container repository. Replace `{REPO_NAME}` with the name of your repository, for example: "myproject/api".

```ssh
aws ecr create-repository --repository-name {REPO_NAME}
```

Optionally, add a lifecycle management policy to the repository to delete older builds. This example sets a retention limit of 250, but you can adjust to any values between 1 and 1000.

```ssh
aws ecr put-lifecycle-policy --registry-id {REPO_ID} --repository-name {REPO_NAME} --lifecycle-policy-text '{"rules":[{"rulePriority":10,"description":"Expire old images","selection":{"tagStatus":"any","countType":"imageCountMoreThan","countNumber":250},"action":{"type":"expire"}}]}'
```

## Configuration

Configuration files for CircleCI can be found in `.circleci/`.

Add your git repository as a project to CircleCI.

Go to "Project Settings" > "Environment Variables" and add values for the following:

* `AWS_ACCOUNT_ID`
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `AWS_REGION`
* `AWS_ECR_ACCOUNT_URL` (this will be the domain section of your ECR repository URL)
* `AWS_REPO` (this will be the ECR repository name, the path section of your ECR repository URL)

## Workflows

The default configuration has two jobs. The first will install the python dependencies and run the project's unit tests. If that job passes, the second job will build a new Docker image and push it to AWS ECR.
