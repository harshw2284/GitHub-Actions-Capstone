# Java Maven CI/CD pipeline

A minimal Java Maven application used to demonstrate a full **GitHub Actions
CI/CD pipeline** built with **reusable workflows**:

1. **Test** – runs JUnit 5 unit tests + a Checkstyle code-quality check
2. **Build** – builds a Docker image from the app using a multi-stage `Dockerfile`
3. **Push** – pushes the built image to Docker Hub

## Project structure

```
.
├── pom.xml
├── Dockerfile
├── .dockerignore
├── config/
│   └── checkstyle.xml
├── src/
│   ├── main/java/com/example/app/App.java
│   ├── main/java/com/example/app/Calculator.java
│   └── test/java/com/example/app/CalculatorTest.java
└── .github/workflows/
    ├── main.yml              # orchestrator (calls the 3 reusable workflows)
    ├── test-reusable.yml     # reusable: test + code quality
    ├── build-reusable.yml    # reusable: docker build
    └── push-reusable.yml     # reusable: docker push
```

## Run it locally

```bash
mvn clean test           # run unit tests
mvn checkstyle:check     # run code quality check
mvn clean package        # build the jar (target/app.jar)
java -jar target/app.jar # run it

docker build -t java-maven-cicd-demo:local .
docker run --rm java-maven-cicd-demo:local
```

## How the pipeline works

`main.yml` is the entry point that GitHub Actions triggers on every push/PR to
`main`. It chains three **reusable workflows** together with `needs:`, so each
stage only runs if the previous one succeeded:

```
test  --->  build  --->  push
```

- `test` and `build` run on every push and pull request.
- `push` only runs on a direct push to `main` (not on PRs), so Docker Hub only
  ever receives images built from `main`.
- The Docker image is built once in the `build` job, saved as a `.tar` file,
  and uploaded as a workflow **artifact**. The `push` job downloads that exact
  artifact, `docker load`s it, and pushes it — guaranteeing the image that
  gets pushed is the exact one that was built and tested, not a rebuild.

## Required GitHub setup

Before the pipeline can push images, add these **repository secrets**
(Settings → Secrets and variables → Actions → New repository secret):

| Secret name           | Value                                                              |
|------------------------|---------------------------------------------------------------------|
| `DOCKERHUB_USERNAME`   | Your Docker Hub username                                            |
| `DOCKERHUB_TOKEN`      | A Docker Hub [access token](https://hub.docker.com/settings/security) (not your password) |

No other configuration is required — `GITHUB_TOKEN` for checkout/artifacts is
provided automatically by GitHub Actions.

## Customizing

- Change the image name/tag in `main.yml` under the `with:` blocks.
- Add more Checkstyle rules in `config/checkstyle.xml`.
- Add a `main` branch protection rule requiring the `test` job to pass before
  merging PRs.
- To push on version tags instead of every commit to `main`, change the `on:`
  trigger and the `if:` condition on the `push` job (e.g. `startsWith(github.ref, 'refs/tags/v')`).

