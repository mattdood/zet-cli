# Zet CLI
A Zettlekasten helper utility.

<img src="https://img.shields.io/github/issues/mattdood/zet-cli"
    target="https://github.com/mattdood/graph-ein/issues"
    alt="Badge for GitHub issues."/>
<img src="https://img.shields.io/github/forks/mattdood/zet-cli"
    target="https://github.com/mattdood/zet-cli/forks"
    alt="Badge for GitHub forks."/>
<img src="https://img.shields.io/github/stars/mattdood/zet-cli"
    alt="Badge for GitHub stars."/>
<img src="https://img.shields.io/github/license/mattdood/zet-cli"
    target="https://github.com/mattdood/zet-cli/raw/master/LICENSE"
    alt="Badge for GitHub license, MIT."/>
<img src="https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2Fmattdood%2Fzet-cli"
    target="https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fmattdood%2Fzet-cli"
    alt="Badge for sharable Twitter link."/>
[![Pytest](https://github.com/mattdood/zet-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/mattdood/zet-cli/actions/workflows/ci.yml)


## Installation
To install the project, run the following:

```
pip install zet-cli
```

## Usage
The commands are well documented using `--help`.

```
zet --help
```

## Concepts
This note taking tool has a few concepts and vocabulary words that should be
understood before utilizing the various commands that are offered.

### Notes
A "zet" is a notes file that is created and stored in a "repo" (folder).
These notes are in Markdown format; however, user created templates
can be created that have different formats.

Any containing assets for a note (images, gifs, etc.) are recommended
to be stored in the folder created specifically for that note. This
allows local references within the Markdown file and helps with
organization when repos contain many zets.

### Repos (Storage)
Each zet file is stored in a date-time folder hierarchy.
Example execution:

```
zet create -t "sample title" -c "sample" -tag "test, test1"
```

Folder structure created:

```
zets/
    2022/
        06/
            01/
                20220601120100/
                            sample-title-20220601120100.md
```

Users can have multiple repos, each with their own zets.
Zets are stored with categories and tags as metadata. Based on the
above sample, the file would have the following information:

```
---
path: '/2022/6/sample-title-20220601120100'
title: 'sample title'
category: 'sample'
tags: ['test', 'test1']
---

# sample title
```

### Templates
A template is provided with the default installation (named "default").
This is referenced within the settings file (`~/zets/.env/.local.json`)
when calling the `zet create` command.

The template can be customized at the path that it is referenced in the
settings file; however, users are encouraged to only modify copies of the template.

For users that wish to provide their own templates, these can be created
then added to the settings file with a path that points to that template.

The settings section goes into greater detail regarding things like defaults
and concepts about modifying default command behavior.

Creating new templates is typically a good idea if other file formats are required,
or if there are fields in the default template that you would like to omit.

**Currently supported fields:**
```
path: 'templatePath'
title: 'templateTitle'
date: 'templateDate'
category: 'templateCategory'
tags: templateTags
```

The `templatePath` is useful for blogging, it has a less verbose structure
than the folder layouts provided by the `zet create` option.

### Git commands
The Zet-CLI offers wrappers around common Git commands to encourage
versioning of notes utilizing Git. This helps to track changes in the notes
repositories over time, while offering simple wrappers to reference repository
locations by name rather than managing the git operations from within the
containing folder.

### Settings
Users have local settings generated at runtime of the CLI. This ensures that
default settings exist and that the folder structure is consistent across installations.

These settings can be modified to change default behaviors, or even copied over from
other installations on separate machines.

**Note:** A potential solution to having multiple solutions may be storing the settings
in a private Gist (if on GitHub) to better keep these installations "in sync".

#### Defaults
The application utilizes defaults to check for things like editors, reduce the
need to specify a specific repo on every command, and determine a template to use
for creating a zet file.

**Note:** The default editor setting is [Neovim](https://neovim.io/).

#### Repos
The repos known to the CLI are referenced here. Repos can exist outside of the
installation directory (`~/zets/`)

Default template names can be altered within the repo record in the settings file.
There is not a CLI option for this.

#### Templates
Templates are used as a base form when creating a new zet. These are copied
and renamed in-place when creating a directory to hold a new zet file. To create
your own templates, utilize the same delimeter pattern (`---`) then place your
corresponding data keys into the file.

These templates do not have to live inside the installation pathway; however,
for organization it is encouraged. A good idea would be to create a `templates/`
directory inside of the environment variables folder (`.env/templates/`).

Templates are referenced by name from the settings file, if you prefer a new default
template then simply change the `defaults` section of the settings file to reference
the name of your new template.

When a template is added to the settings file it will become available in the
CLI for creating zets.

**Note:** All templates need their full directory listed in settings. This should
include an absolute reference.

Example:
```
"templates": {
    "default": ...,
    "my_template": "~/zets/.env/templates/my-template.md"
}
```

## Running tests
To run the test suite we need to tell the settings to use a different installation
location or we'll run into clashing with any other installations. This could
result in deleting your note repos, settings, etc.

Running the test suite with a `ZET_STAGE=test` will ensure the installation
pathway of the test objects is inside the project, where teardown can safely take place.

```bash
ZET_STAGE=test pytest -vv -s
```

## Releasing builds
To release builds for the project we use a combination of tagging and changes to
`setup.py`.

For any releases to `test.pypi.org` use a change to the `version="..."` inside of
`setup.py`. Once a PR is merged into the main project the test release will be updated.

Any prod releases to `pypi.org` require a tagged version number. This should be done locally
by running the following:

```bash
git checkout master
git pull master
git tag v<version-number-here>
git push origin v<version-number-here>
```

### Rollbacks of versions
To roll a version back we need to delete the tagged release from the prod PyPI,
then delete the GitHub tag.

```
git tag -d v<version-number-here>
git push origin :v<version-number-here>
```

