# Recommended Git Flow

The recommended gitflow for this project is as follows:

* Two long-term branches:
  * `main`
  * `dev`
* The `main` branch should always be deployable
* The `dev` branch is used for feature testing and should be deployed to an internal/protected domain
* Features should belong to short-lived feature branches based on `main`
* Feature branches should be merged into the `dev` for user testing
* Feature branches should be merged into the `main` branch for QA/Prod deployment
* Feature branches should be removed once successfully deployed to Prod
* The `dev` should be reset to `main` from time-to-time to keep it clean
* Releases for QA/Prod must be based on the `main` branch, and tagged with 'release-\*.\*.\*' using major-minor-revision notation

## Starting a New Feature

Create a new branch off `main`:

```ssh
$ git checkout main
$ git checkout -b <feature-name>
```

If this is a medium- to long-term feature that should be tracked remotely, push it to the remote repository:

```ssh
$ git push --set-upstream origin <feature-name>
```

## Testing a Feature on Dev

```ssh
$ git checkout dev
$ git merge <feature-name> -m <commit-message>
$ git push origin
```

If you are using the default CircleCI configuration, this will build a development Docker image and push it to AWS ECR where it can be deployed manually to an internal dev server for feature testing.

## Creating a New Feature Release

### Rebase (optional)

If the feature branch and `main` commit histories have drifted apart, you may want to rebase the feature branch using `main` to make the merge easier:

```ssh
$ git checkout <feature-name>
$ git pull --rebase origin main
```

### Merge

To keep the commit history of the feature branch, merge it into `main`:

```ssh
$ git checkout main
$ git merge <feature-name> -m <commit-message> 
$ git push origin
```

Or to flatten the commit history into a single commit, use the `squash` flag when merging into `main`:

```ssh
$ git checkout main
$ git merge --squash <feature-name>
$ git commit -m <commit-message>
$ git push origin
```

### Tag

Tag the release. Release tags should use semantic versioning, following the format: 'release-\*.\*.\*' (major.minor.revision).

```ssh
$ git tag -a <release-tag> -m <tag-message>
$ git push origin <release-tag>
```

If you are using the default CircleCI configuration, this will build a production-ready Container image and push it to AWS ECR where it can be deployed manually.

## Removing an Old Feature Branch

```ssh
$ git push -d origin <feature-name>
$ git branch -D <feature-name>
```

## Reset Dev Branch to Main

```ssh
$ git checkout dev
$ git fetch origin
$ git reset --hard main
```
