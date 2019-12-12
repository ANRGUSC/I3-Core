# Contributing to I3 SDK

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to I3 SDK, which are hosted in the [I3-SDK](https://github.com/ANRGUSC/I3-SDK) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

#### Table Of Contents

[Code of Conduct](#code-of-conduct)

[I don't want to read this whole thing, I just have a question!!!](#i-dont-want-to-read-this-whole-thing-i-just-have-a-question)

[What should I know before I get started?](#what-should-i-know-before-i-get-started)
  * [I3 - Core and SDK](https://github.com/ANRGUSC/iotm)

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Your First Code Contribution](#your-first-code-contribution)
  * [Pull Requests](#pull-requests)

[Styleguides](#styleguides)
  * [Git Commit Messages](#git-commit-messages)
  * [Documentation Styleguide](#documentation-styleguide)

[Additional Notes](#additional-notes)
  * [Issue and Pull Request Labels](#issue-and-pull-request-labels)

## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [karya@usc.edu](mailto:karya@usc.edu).

## I don't want to read this whole thing I just have a question!!!

## What should I know before I get started?

### I3

The Intelligent IoT Integrator (I3) is a community data exchange marketplace platform being developed at the University of Southern California, with support from the City of LA and other organizations, to help enable exchange of real-time IoT data for smart cities (see https://i3.usc.edu/ for details). While the I3 platform itself is still under development, we are pleased to provide a sandbox pre-release alpha instance of I3 that you can use to publish and subscribe to diverse IoT data streams. 

Technically, I3 includes both a web-based marketplace and a publish-subscribe broker. The web-marketplace is where data products can be posted by "sellers" and browsed and selected by "buyers" and can be accessed both manually through the site and automatically through a REST API. Although it allows sellers to specify the unit price of data, real payment channels are currently disabled in I3. The publish-subscribe system is based on MQTT, and can be accessed through MQTT SDK's as well as a REST-based wrapper. For maximum flexibility, I3 is agnostic to the data model being used, the data streams sent over I3 can be in any JSON-formatted model, with the seller posting information on the particular data format/model used so that the buyer knows how to interpret the feed they subscribe to. Currently, as it is built on top of MQTT which is intended for more lightweight IoT applications, I3 does not support heavy-duty data streams such as videos.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report :pencil:, reproduce the behavior :computer: :computer:, and find related reports :mag_right:.

Before creating bug reports, please check as you might find out that you don't need to create one. When you are creating a bug report, please [include as many details as possible](#how-do-i-submit-a-good-bug-report). Fill out [the required template](https://github.com/ANRGUSC/I3-SDK/blob/master/docs/issue-template.md), the information it asks for helps us resolve issues faster.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.


#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/). After you've determined the branch your bug is related to, create an issue on that repository and provide the following information by filling in [the template](https://github.com/ANRGUSC/I3-SDK/blob/master/docs/issue-template.md).

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible. For example, start by explaining how you started I3, e.g. which command exactly you used in the terminal, or how you started I3 otherwise. When listing steps, **don't just say what you did, but explain how you did it**.
* **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples. If you're providing snippets in the issue.
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Include screenshots and animated GIFs** which show you following the described steps and clearly demonstrate the problem. 
* **If the problem wasn't triggered by a specific action**, describe what you were doing before the problem happened and share more information using the guidelines below.

Provide more context by answering these questions:

* **Did the problem start happening recently** (e.g. after updating to a new version) or was this always a problem?
* If the problem started happening recently, **can you reproduce the problem in an older version?** What's the most recent version in which the problem doesn't happen?
* **Can you reliably reproduce the issue?** If not, provide details about how often the problem happens and under which conditions it normally happens.
* If the problem is related to working with files (e.g. opening and editing files), **does the problem happen for all files and projects or only some?** 

Include details about your configuration and environment:

* **Which version you are using?**
* **What's the name and version of the OS you're using**?
* **Are you running I3 locally in a virtual machine or a test instance?** If so, which VM software are you using and which operating systems and versions are used for the host and the guest? If using a hosted I3 instance, please mention the host, port and other details.
* **Are you using I3 SDK with multiple publish subscriber?** If so, can you reproduce the problem with a single script?

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for I3 SDK, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion :pencil: and find related suggestions :mag_right:.

Before creating enhancement suggestions, please check as you might find out that you don't need to create one. When you are creating an enhancement suggestion, please [include as many details as possible](#how-do-i-submit-a-good-enhancement-suggestion). Fill in [the template](https://github.com/ANRGUSC/I3-SDK/blob/master/docs/feature_request.md), including the steps that you imagine you would take if the feature you're requesting existed.

#### Before Submitting An Enhancement Suggestion

* **Check if there's already existing request which provides that enhancement.**
* **Determine which repository the enhancement should be suggested in.**
* **Perform a [cursory search](https://github.com/search?q=+is%3Aissue+user%3Ai3-sdk)** to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/). After you've determined which branch your enhancement suggestion is related to, create an issue on that repository and provide the following information:

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples, as [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Include screenshots and animated GIFs** which help you demonstrate the steps or point out the part I3 which the suggestion is related to. You can use [this tool](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux.
* **Explain why this enhancement would be useful** 
* **List some other mqtt subcriber or applications where this enhancement exists.**
* **Specify which version of I3 SDK you're using.** 
* **Specify the name and version of the OS you're using.**

### Your First Code Contribution

Unsure where to begin contributing to I3 SDK? I3 SDK is a beginner friendly open source project. You can start by looking through these `beginner` and `help-wanted` issues:

* [Beginner issues][beginner] - issues which should only require a few lines of code, and a test or two.
* [Help wanted issues][help-wanted] - issues which should be a bit more involved than `beginner` issues.


If you want to read about using I3, the [I3](https://i3.usc.edu/) and I3 is free and available online [I3](https://github.com/ANRGUSC/iotm).

#### Local development

I3 Core and all I3-SDK can be developed locally and tested. For instructions on how to do this, see the following sections in the [I3](https://github.com/ANRGUSC/iotm)

### Pull Requests

The process described here has several goals:

- Maintain code quality
- Fix problems that are important to users
- Engage the community in working toward the best possible result
- Enable a sustainable system for the maintainers to review contributions

Please follow these steps to have your contribution considered by the maintainers:

1. Follow all instructions in [the template](PULL_REQUEST_TEMPLATE.md)
2. After you submit your pull request, verify that all [status checks](https://help.github.com/articles/about-status-checks/) are passing <details><summary>What if the status checks are failing?</summary>If a status check is failing, and you believe that the failure is unrelated to your change, please leave a comment on the pull request explaining why you believe the failure is unrelated. A maintainer will re-run the status check for you. If we conclude that the failure was a false positive, then we will open an issue to track that problem with our status check suite.</details>

While the prerequisites above must be satisfied prior to having your pull request reviewed, the reviewer(s) may ask you to complete additional design work, tests, or other changes before your pull request can be ultimately accepted.

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood 
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
    * :art: `:art:` when improving the format/structure of the code
    * :racehorse: `:racehorse:` when improving performance
    * :non-potable_water: `:non-potable_water:` when plugging memory leaks
    * :memo: `:memo:` when writing docs
    * :penguin: `:penguin:` when fixing something on Linux
    * :apple: `:apple:` when fixing something on macOS
    * :checkered_flag: `:checkered_flag:` when fixing something on Windows
    * :bug: `:bug:` when fixing a bug
    * :fire: `:fire:` when removing code or files
    * :green_heart: `:green_heart:` when fixing the CI build
    * :white_check_mark: `:white_check_mark:` when adding tests
    * :lock: `:lock:` when dealing with security
    * :arrow_up: `:arrow_up:` when upgrading dependencies
    * :arrow_down: `:arrow_down:` when downgrading dependencies
    * :shirt: `:shirt:` when removing linter warnings


## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help us track and manage issues and pull requests. 

The labels are loosely grouped by their purpose, but it's not required that every issue have a label from every group or that an issue can't have more than one label from the same group.

Please open an issue on `I3` if you have suggestions for new labels.

#### Type of Issue and Issue State

| Label name | `I3` | Description |
| --- | --- | --- | 
| `enhancement` | [search][search-i3-label-enhancement] | Feature requests. |
| `bug` | [search][search-i3-label-bug] | Confirmed bugs or reports that are very likely to be bugs. |
| `question` | [search][search-i3-label-question] | Questions more than bug reports or feature requests (e.g. how do I do X). |
| `feedback` | [search][search-i3-label-feedback] | General feedback more than bug reports or feature requests. |
| `help-wanted` | [search][search-i3-label-help-wanted] | The core team would appreciate help from the community in resolving these issues. |
| `beginner` | [search][search-i3-label-beginner] | Less complex issues which would be good first issues to work on for users who want to contribute. |
| `more-information-needed` | [search][search-i3-label-more-information-needed] | More information needs to be collected about these problems or feature requests (e.g. steps to reproduce). |
| `needs-reproduction` | [search][search-i3-label-needs-reproduction] | Likely bugs, but haven't been reliably reproduced. |
| `blocked` | [search][search-i3-label-blocked] | Issues blocked on other issues. |
| `duplicate` | [search][search-i3-label-duplicate] | Issues which are duplicates of other issues, i.e. they have been reported before. |
| `wontfix` | [search][search-i3-label-wontfix] | The core team has decided not to fix these issues for now, either because they're working as intended or for some other reason. |
| `invalid` | [search][search-i3-label-invalid] | Issues which aren't valid (e.g. user errors). |


#### Pull Request Labels

| Label name | I3 SDK :mag_right: | Description
| --- | --- | --- |
| `work-in-progress` | [search][search-i3-label-work-in-progress] | Pull requests which are still being worked on, more changes will follow. |
| `needs-review` | [search][search-i3-label-needs-review] | Pull requests which need code review, and approval from maintainers or core team. |
| `under-review` | [search][search-i3-label-under-review] | [search][search-i3-label-under-review] | Pull requests being reviewed by maintainers or core team. |
| `requires-changes` | [search][search-i3-label-requires-changes] | Pull requests which need to be updated based on review comments and then reviewed again. |
| `needs-testing` |  [search][search-i3-label-needs-testing] | Pull requests which need manual testing. |

Referenced from https://github.com/atom
