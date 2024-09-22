# Advanced Usage and Customization

As you become more familiar with Cosmosys, you may find yourself wanting to leverage its more advanced features and customize it further to fit your specific needs. This guide will explore some of the more sophisticated capabilities of Cosmosys and provide tips for power users.

## Advanced Configuration

### Environment-Specific Configurations

Cosmosys allows you to have different configurations for different environments. You can use environment variables in your `cosmosys.toml` file:

```toml
[project]
name = "${PROJECT_NAME}"
version = "${PROJECT_VERSION}"

[git]
remote = "${GIT_REMOTE:-origin}"
```

Then, set these environment variables before running Cosmosys.

### Dynamic Step Selection

You can dynamically select which steps to run based on conditions:

```toml
[release]
steps = [
    "version_update",
    "changelog_update",
    { step = "run_tests", condition = "${RUN_TESTS:-true}" },
    "git_commit",
    { step = "publish_pypi", condition = "${PUBLISH_PYPI:-false}" }
]
```

### Custom Version Schemes

While Cosmosys uses semantic versioning by default, you can implement custom version schemes:

```toml
[version]
scheme = "custom"
pattern = "v{year}.{month}.{build}"
```

You'll need to implement a custom version update step to handle this scheme.

## Advanced Git Integration

### Multiple Remotes

Cosmosys can work with multiple Git remotes:

```toml
[git]
remotes = ["origin", "upstream"]
push_to = ["origin"]
```

### Branch-Specific Behavior

Configure different behavior based on the current Git branch:

```toml
[git.branches.main]
tag = true
push = true

[git.branches.develop]
tag = false
push = true
```

## Custom Release Steps

### Implementing Complex Steps

For more complex release steps, you can create a custom plugin. Here's an advanced example that integrates with a hypothetical deployment service:

```python
import requests
from cosmosys.steps.base import Step, StepFactory
from cosmosys.config import CosmosysConfig

@StepFactory.register("deploy_to_service")
class DeployToServiceStep(Step):
    def __init__(self, config: CosmosysConfig):
        super().__init__(config)
        self.api_key = os.environ.get("DEPLOY_SERVICE_API_KEY")
        self.service_url = config.get("deploy.service_url")

    def execute(self) -> bool:
        if not self.api_key or not self.service_url:
            self.log("Missing API key or service URL")
            return False

        response = requests.post(
            f"{self.service_url}/deploy",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"version": self.config.project.version}
        )

        if response.status_code == 200:
            self.log("Deployment successful")
            return True
        else:
            self.log(f"Deployment failed: {response.text}")
            return False

    def rollback(self) -> None:
        # Implement rollback logic here
        pass
```

## Advanced Changelog Management

### Custom Changelog Templates

Cosmosys allows for custom changelog templates. Create a file named `changelog_template.md`:

```markdown
# Changelog

## [{{version}}] - {{date}}

{{#each categories}}
### {{name}}

{{#each entries}}
- {{this}}
{{/each}}

{{/each}}
```

Then, reference it in your `cosmosys.toml`:

```toml
[changelog]
template = "changelog_template.md"
```

### Automatic Issue Linking

Configure Cosmosys to automatically link issues in your changelog:

```toml
[changelog]
issue_url = "https://github.com/your-repo/issues/{}"
```

This will turn mentions like "#123" into clickable links in your changelog.

## Integrating with External Tools

### Slack Notifications

Create a custom step to send Slack notifications about your release:

```python
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from cosmosys.steps.base import Step, StepFactory

@StepFactory.register("slack_notify")
class SlackNotifyStep(Step):
    def execute(self) -> bool:
        client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
        try:
            response = client.chat_postMessage(
                channel="releases",
                text=f"New release: {self.config.project.name} v{self.config.project.version} is now available!"
            )
            return True
        except SlackApiError as e:
            self.log(f"Error sending Slack message: {e}")
            return False
```

## Performance Optimization

### Parallel Execution

For projects with many independent release steps, you can implement parallel execution:

```python
import concurrent.futures
from cosmosys.release import ReleaseManager

class ParallelReleaseManager(ReleaseManager):
    def execute_steps(self, steps: List[str], dry_run: bool) -> bool:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.execute_step, step, dry_run) for step in steps]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        return all(results)
```

## Security Considerations

### Signing Releases

Implement a step to cryptographically sign your releases:

```python
import gnupg
from cosmosys.steps.base import Step, StepFactory

@StepFactory.register("sign_release")
class SignReleaseStep(Step):
    def execute(self) -> bool:
        gpg = gnupg.GPG()
        with open(f"{self.config.project.name}-{self.config.project.version}.tar.gz", "rb") as f:
            signed_data = gpg.sign_file(f, keyid="YOUR_GPG_KEY_ID", passphrase="YOUR_PASSPHRASE")
        
        if signed_data.status == "signature created":
            with open(f"{self.config.project.name}-{self.config.project.version}.tar.gz.asc", "w") as f:
                f.write(str(signed_data))
            return True
        else:
            self.log(f"Failed to sign release: {signed_data.status}")
            return False
```
