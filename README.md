<p align="center">
  <a href="https://joanroig.github.io/metrix-gallery">
  <img alt="Metrix Generated Header" src="https://raw.githubusercontent.com/joanroig/metrix/metrix-header-only/metrix-header.gif">
  </a>
</p>

<p align="center">Metrix generates a customizable retro-style GIF infographic showcasing GitHub metrics for your GitHub README profile. Choose your color combination with the <a href="https://joanroig.github.io/metrix-gallery">Metrix Gallery</a>.
</p>

<table align="center">
  <tr>
    <td align="center">
      <a href="#default"><img src="img/metrix-default.gif" width="240px" /></a>
    </td>
    <td align="center">
      <a href="#red"><img src="img/metrix-red.gif" width="240px" /></a>
    </td>
    <td align="center">
      <a href="#blue"><img src="img/metrix-blue.gif" width="240px" /></a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="#default"><b>Default</b></a>
    </td>
    <td align="center">
      <a href="#red"><b>Red</b></a>
    </td>
    <td align="center">
      <a href="#blue"><b>White-Blue</b></a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="#yellow-noglitch"
        ><img src="img/metrix-yellow-noglitch.gif" width="240px"
      /></a>
    </td>
    <td align="center">
      <a href="#gold-customtext"
        ><img src="img/metrix-gold-customtext.gif" width="240px"
      /></a>
    </td>
    <td align="center">
      <a href="#purple-torvalds"
        ><img src="img/metrix-purple-torvalds.gif" width="240px"
      /></a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="#yellow-noglitch"><b>Yellow No-Glitch</b></a>
    </td>
    <td align="center">
      <a href="#gold-customtext"><b>Gold Custom Text</b></a>
    </td>
    <td align="center">
      <a href="#purple-torvalds"><b>Purple Torvalds</b></a>
    </td>
  </tr>
</table>

## Usage Guide

Follow these steps to integrate Metrix into your GitHub profile:

1.  **Create a New Repository**  
    Create a new repository to host your profile README. For guidance, refer to GitHub’s documentation on [setting up and managing your profile README](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme).

2.  **(Optional) Generate and Add a Personal Access Token (PAT)**  
    By default, the action will only display public data. To also include private repository data, follow these steps:

    1. Create a PAT token from [GitHub's Token Settings](https://github.com/settings/tokens) with the following permissions:

       - **repo**: Full control of private repositories
       - **read:org**: Read org and team membership, and org projects
       - **read:user**: Read all user profile data

    2. In your repository, navigate to **Settings > Secrets and variables** and add a new secret:

       - Name the secret `PAT_TOKEN`
       - Paste the PAT token value generated in the previous step

    In your repository settings, go to **Settings > Actions > General** and enable **"Read repository contents and packages permissions"** at the bottom of the page.3. **Enable Workflow Permissions**

3.  **Add the Metrix GIF to Your README** \*  
     Create a new `README.md` like this: Create a new `README.md` like this:

    ````markdown
    <p align="center">
      <a href="https://github.com/joanroig/metrix" title="View Metrix on GitHub">om/joanroig/metrix" title="View Metrix on GitHub">
        <img src="metrix.gif"/>mg src="metrix.gif"/>
      </a>
      <br/>
      <sub>Infographic generated with <a href="https://github.com/joanroig/metrix">joanroig/metrix</a></sub>ub>Infographic generated with <a href="https://github.com/joanroig/metrix">joanroig/metrix</a></sub>
    </p>>
    ```    ```

    Or add the following to your `README.md` file: Or add the following to your `README.md` file:

    ```markdown
    [![metrix](metrix.gif)](https://github.com/joanroig/metrix)metrix](metrix.gif)](https://github.com/joanroig/metrix)
    `    `

    You can see a live example here: https://github.com/joanroig/joanroig/blob/main/README.md You can see a live example here: https://github.com/joanroig/joanroig/blob/main/README.md
    ```
    ````

4.  **Create a GitHub Action**  
     In your repository, create a new file at `.github/workflows/metrix.yml` and paste the following content:
    e a GitHub Action\*_  
     ```yaml a new file at `.github/workflows/metrix.yml` and paste the following content:
    name: Generate Metrics GIF
    yaml
    on: # Run manually from the Actions tab
    workflow_dispatch: # Run on schedule (adjust as needed)ually from the Actions tab
    schedule: - cron: "0 0 _ _ 0" # Weekly on Sundays at midnight # Run on schedule (adjust as needed)
    edule:
    jobs: "0 0 _ \* 0" # Weekly on Sundays at midnight
    generate:
    runs-on: ubuntu-latest
    steps: - name: Generate Metrix
    uses: joanroig/metrix@main
    with:
    GITHUB_TOKEN: ${{ secrets.PAT_TOKEN || secrets.GITHUB_TOKEN }}
    GITHUB_USERNAME: ${{ github.actor }} # You can add more customization parameters here GITHUB_TOKEN: ${{ secrets.PAT_TOKEN || secrets.GITHUB_TOKEN }}

    ````GITHUB_USERNAME: ${{ github.actor }}

        You can find an example with all the default configuration in the [metrix-complete.yml](.github/workflows/metrix-complete.yml) file.    ```

        Your action is now set up! Commit the changes and manually trigger the action to generate the metrics GIF.6.  **Run the Action**  metrix-complete.yml) file.

        You can use the [metrix-complete.yml](.github/workflows/metrix-complete.yml) file or read the [parameters](#parameters) section to find some parameters to add and customize in your action. Lots of interesting color combinations can be found using the <a href="https://joanroig.github.io/metrix-gallery">Metrix Gallery</a>.7.  **(Optional) Customize your Metrix**

    tion is now set up! Commit the changes and manually trigger the action to generate the metrics GIF.
    ````

## Showcase

ustomize your Metrix\*\*

<p align="center">rkflows/metrix-complete.yml) file or read the [parameters](#parameters) section to find some parameters to add and customize in your action. Lots of interesting color combinations can be found using the <a href="https://joanroig.github.io/metrix-gallery">Metrix Gallery</a>.
<a href="https://joanroig.github.io/metrix-gallery">
  <img alt="Showcase" src="showcase.gif">wcase
  </a>
</p><p align="center">

Some examples are provided below, with the corresponding configuration for each: <img alt="Showcase" src="showcase.gif">
/a>
---</p>

### <a id="default"></a> DefaultSome examples are provided below, with the corresponding configuration for each:

> Notice that looping is deactivated by default!---

![default](img/metrix-default.gif)### <a id="default"></a> Default

```ice that looping is deactivated by default!
with:
  GITHUB_USERNAME: 'joanroig'efault](img/metrix-default.gif)
```

---with:
roig'

### <a id="red"></a> Red```

![red](img/metrix-red.gif)---

````a id="red"></a> Red
with:
  GITHUB_USERNAME: 'joanroig'ed.gif)
  TEXT_COLOR: 'red'
  LOOP: 'true'
```with:
ITHUB_USERNAME: 'joanroig'
---  TEXT_COLOR: 'red'

### <a id="blue"></a> White over blue```

![blue](img/metrix-blue.gif)---

```a id="blue"></a> White over blue
with:
  GITHUB_USERNAME: 'joanroig'f)
  BACKGROUND_COLOR: 'blue'
  TEXT_COLOR: 'white'
  LOOP: 'true'h:
```  GITHUB_USERNAME: 'joanroig'
ACKGROUND_COLOR: 'blue'
---  TEXT_COLOR: 'white'

### <a id="yellow-noglitch"></a> Yellow with disabled glitches```

![yellow noglitch](img/metrix-yellow-noglitch.gif)---

```a id="yellow-noglitch"></a> Yellow with disabled glitches
with:
![yellow noglitch](img/metrix-yellow-noglitch.gif)
  GITHUB_USERNAME: 'joanroig'
  TEXT_COLOR: 'yellow'
  GLITCHES: 'false'
  LOOP: 'true'ITHUB_USERNAME: 'joanroig'
```  TEXT_COLOR: 'yellow'
LITCHES: 'false'
---  LOOP: 'true'

### <a id="gold-customtext"></a> Gold over dark gold, with custom texts

![gold customtext](img/metrix-gold-customtext.gif)
 <a id="gold-customtext"></a> Gold over dark gold, with custom texts
````

with:-gold-customtext.gif)
GITHUB_USERNAME: 'joanroig'
BACKGROUND_COLOR: 'darkgoldenrod'
TEXT_COLOR: 'gold'
ACTIVITY_TEXT: 'I worked a lot lately...'USERNAME: 'joanroig'
TEXT: |od'
{username} is booting up......
----------------------- ACTIVITY_TEXT: 'I worked a lot lately...'

Joined GitHub {created_at}.
Followed by {followers} Users
Owner of {total_repos} Repos

Total Commits: {total_commits}ers
Total Stars: {total_stars} Owner of {total_repos} Repos

Data updated: {updated_date}s: {total_commits}
LOOP: 'true'otal Stars: {total_stars}

```
ata updated: {updated_date}
---  LOOP: 'true'

### <a id="purple-torvalds"></a> Yellow over purple, with data from another user, reduced activity days, and custom activity text

![default](img/metrix-purple-torvalds.gif)
 <a id="purple-torvalds"></a> Yellow over purple, with data from another user, reduced activity days, and custom activity text
```

with:torvalds.gif)
GITHUB_USERNAME: 'torvalds'
TEXT_COLOR: 'yellow'
BACKGROUND_COLOR: 'purple'
ACTIVITY_TEXT: 'Last two weeks were intense:'orvalds'
ACTIVITY_DAYS: '14''yellow'
LOOP: 'true'ACKGROUND_COLOR: 'purple'

```ACTIVITY_TEXT: 'Last two weeks were intense:'
CTIVITY_DAYS: '14'
---  LOOP: 'true'
```

---

### <a id="customsize"></a> A gif with a custom size, a bigger font size, only text, a custom cursor and a generative text color shade based on a random light background color

### <a id="customsize"></a> A gif with a custom size, a bigger font size, only text, a custom cursor and a generative text color shade based on a random light background color

![customsize](img/metrix-customsize.gif)with:
ONT_SIZE: '29',

```KGROUND_COLOR: 'random-light',
with:de',
  FONT_SIZE: '29',e customized!',
  BACKGROUND_COLOR: 'random-light',',
  TEXT_COLOR: 'shade',
  TEXT: 'The size of the gif\ncan be customized!',
  TYPING_CHARACTER: '|',
  ACTIVITY: 'false',
  LOOP: 'true'
  WIDTH: '580'
  HEIGHT: '80'
```

## <a id="parameters"></a>Available Parameters and Options

nts. A complete example, including the default parameters, is provided: [metrix-complete.yml](.github/workflows/metrix-complete.yml). Below is the full list of available parameters:

## <a id="parameters"></a>Available Parameters and Options

                                                    |

Metrix is highly customizable through GitHub Action arguments. A complete example, including the default parameters, is provided: [metrix-complete.yml](.github/workflows/metrix-complete.yml). Below is the full list of available parameters:| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |

| **Parameter**                                                      | **Description**                                                                                                                                    | **Example/Options**                                                                                                    |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | --------- | ----------------- | --------------------------------------- | --------------------- |
| GITHUB_TOKEN                                                       | GitHub token used for authentication. Defaults to `PAT_TOKEN` if available.                                                                        | `${{ secrets.PAT_TOKEN \|\| secrets.GITHUB_TOKEN }}`                                                                   |
| GITHUB_USERNAME                                                    | GitHub username to display the metrics for.                                                                                                        | `${{ github.actor }}`                                                                                                  |
| LOG_LEVEL                                                          | Application log level.                                                                                                                             | `'NOTSET'`, `'DEBUG'`, `'INFO'`, `'WARNING'`, `'ERROR'`, `'FATAL'`                                                     |
| FFMPEG_LOG_LEVEL                                                   | FFmpeg log level.                                                                                                                                  | `'DEBUG'`, `'VERBOSE'`, `'INFO'`, `'WARNING'`, `'ERROR'`, `'FATAL'`, `'PANIC'`, `'QUIET'`                              |
| FONT_SIZE                                                          | Font size for the main text. Note: Not tested, may cause rendering issues.                                                                         | `'20'`                                                                                                                 |
| SYMBOL_FONT_SIZE                                                   | Font size for symbols. Note: Not tested, may cause rendering issues.                                                                               | `'20'`                                                                                                                 |
| FONT_PATH                                                          | Path to the primary font file. Note: Not tested, may cause rendering issues.                                                                       | `'assets/MxPlus_IBM_BIOS.ttf'`                                                                                         |
| SYMBOL_FONT_PATH                                                   | Path to the symbol font file. Note: Not tested, may cause rendering issues.                                                                        | `'assets/MxPlus_IBM_BIOS.ttf'`                                                                                         |
| BACKGROUND_COLOR                                                   | Background color. Same options as TEXT_COLOR.                                                                                                      | `'red'`,`'#6e2e2a'`,`'random'`, `'random-light'`, `'random-dark'`, `'complementary'`, `'contrasting'`, `'shade'`, etc  |
| TEXT_COLOR                                                         | Color of the text. Options include CSS color names, hex codes, 'random', 'random-light', 'random-dark', 'complementary', 'contrasting' or 'shade'. | `'blue'`,`'#c4a5a3'`,`'random'`, `'random-light'`, `'random-dark'`, `'complementary'`, `'contrasting'`, `'shade'`, etc |
| MINIMUM_CONTRAST                                                   | Minimum contrast ratio between text and background (1 to 21).                                                                                      | `'2'`                                                                                                                  |
| MAX_GLITCHES                                                       | Maximum number of glitches that can occur simultaneously.                                                                                          | `'4'`                                                                                                                  |
| GLITCH_PROBABILITY                                                 | Probability of a glitch occurring in a frame (0 to 100).                                                                                           | `'3'`                                                                                                                  |
| OUTPUT_FILE_PATH                                                   | Path for the generated GIF.                                                                                                                        | `'metrix.gif'`                                                                                                         |           | ACTIVITY          | Enable or disable the activity section. | `'true'` or `'false'` |
| `'Last month commit activity:'`                                    |
| ### <a id="variables"></a>Text Variables (Curated GitHub API Data) | ACTIVITY_DAYS                                                                                                                                      | Number of days for the activity chart.                                                                                 | `'30'`    |
|                                                                    |
| **Variable**                                                       | **Description**                                                                                                                                    | **Example Replacement**                                                                                                | `'false'` |
| -----------------------------------------------------              | ------------------------------------------------------------------------------------                                                               | ----------------------------------                                                                                     |           |
| `{username}`                                                       | GitHub username                                                                                                                                    | `'joanroig'`                                                                                                           |           |
| `{separator}`                                                      | Custom separator for formatting                                                                                                                    | `'------------------------------'`                                                                                     | `'false'` |
| `{updated_date}`                                                   | Date of the latest update                                                                                                                          | `'2025-04-05'`                                                                                                         |
| `{total_repos}`                                                    | Total number of repositories                                                                                                                       | `'42'`                                                                                                                 |
| `{total_commits}`                                                  | Total number of commits                                                                                                                            | `'500'`                                                                                                                |
| `{total_stars}`                                                    | Total number of stars across repositories                                                                                                          | `'150'`                                                                                                                |
| `{total_forks}`                                                    | Total number of forks                                                                                                                              | `'30'`                                                                                                                 |
| `{total_watchers}`                                                 | Total number of watchers                                                                                                                           | `'100'`                                                                                                                |
| `{total_open_issues}`                                              | Total number of open issues                                                                                                                        | `'10'`                                                                                                                 |
| `{preferred_languages}` or `{preferred_languages[X]}`              | Preferred programming languages, where X can be set to a number to limit the results                                                               | `'TypeScript, Python, JavaScript'`                                                                                     |
| `{preferred_topics}` or `{preferred_topics[X]}`                    | Preferred topics, where X can be set to a number to limit the results                                                                              | `'API, Hacking'`                                                                                                       |
| `{preferred_licenses}` or `{preferred_licenses[X]}`                | Preferred license types, where X can be set to a number to limit the results                                                                       | `'MIT','GPL'`                                                                                                          |           | `{total_commits}` | Total number of commits                 | `'500'`               |
| Total number of stars across repositories                          | `'150'`                                                                                                                                            |
| #### Extended Text Variables (Raw GitHub API Data)                 | `{total_forks}`                                                                                                                                    | Total number of forks                                                                                                  | `'30'`    |

These variables are sourced directly from the GitHub User API data without any transformations, except for the reformatting of dates. Please note that this data may change over time, and the variables listed were the ones available at the time of writing:| `{total_open_issues}` | Total number of open issues | `'10'` |
umber to limit the results | `'TypeScript, Python, JavaScript'` |
| **Variable** | **Description** | **Example** |the results | `'API, Hacking'` |
| ----------------------------- | ------------------------------------------ | ----------------------------------- | limit the results | `'MIT','GPL'` |
| `{login}` | GitHub login name | `'joanroig'` |
| `{id}` | Unique GitHub user ID | `'123456789'` |
| `{node_id}` | Node identifier | `'MDQ6VXNlcjEyMzQ1Njc4OQ=='` |
| `{type}` | Type of account (e.g., "User") | `'User'` |matting of dates. Please note that this data may change over time, and the variables listed were the ones available at the time of writing:
| `{user_view_type}` | User view type (e.g., "private") | `'private'` |
| `{site_admin}` | Site administrator status (Boolean) | `'false'` |
| `{name}` | Display name | `'Joan Roig'` |
| `{company}` | Company name (if provided) | `'Company Inc.'` |
| `{blog}` | Blog URL | `'https://blog.example.com'` |
| `{location}` | User location | `'Barcelona, Spain'` |
| `{email}` | Email address (if provided) | `'joan@example.com'` |
| `{hireable}` | Hireable status (if provided) | `'true'` |
| `{bio}` | Biography | `'Software developer and musician'` |
| `{twitter_username}` | Twitter username | `'@joanroig'` |
| `{public_repos}` | Count of public repositories | `'35'` |
| `{public_gists}` | Count of public gists | `'5'` |
| `{followers}` | Number of followers | `'200'` |
| `{following}` | Number of users followed | `'150'` |
| `{created_at}` | Date the GitHub account was created | `'2015-05-17'` |
| `{updated_at}` | Date the GitHub account was last updated | `'2025-04-05'` |
| `{private_gists}` | Count of private gists | `'10'` |
| `{total_private_repos}` | Total number of private repositories | `'10'` |
| `{owned_private_repos}` | Count of owned private repositories | `'5'` |
| `{disk_usage}` | Disk usage in kilobytes | `'50000'` |
| `{collaborators}` | Number of collaborators | `'10'` |
| `{two_factor_authentication}` | Two-factor authentication status (Boolean) | `'true'` || `{created_at}` | Date the GitHub account was created | `'2015-05-17'` |
| Date the GitHub account was last updated | `'2025-04-05'` |

## Development Setup| `{private_gists}` | Count of private gists | `'10'` |

e_repos}`      | Total number of private repositories       |`'10'` |

### Requirements| `{owned_private_repos}` | Count of owned private repositories | `'5'` |

                    | `'50000'`                           |

- **Conda** or **Miniconda** (alternatively, only Python)ators}`            | Number of collaborators                    |`'10'` |
- **FFmpeg**ation status (Boolean) | `'true'` |
- **VSCode** (optional, for debugging and development)
  pment Setup

### Setup

1. Clone this repository and open it in your IDE (e.g., **VSCode**).
2. Add your **PAT** token to the `.github_token` file.
3. If you have **Conda** installed, run `rebuild_env.ps1` to set up the Conda environment, then execute `run.ps1` to start the application. Otherwise, read the two scripts to run the commands using Python.- **FFmpeg**
   and development)

### Running and Debugging with VS Code

The project includes preconfigured launch settings in the `.vscode/launch.json` file that make it easy to run Metrix:

1. **Python: Debug** - Runs the main application with a default configuration
   - Renders a standard Metrix GIF with GitHub user statsonment, then execute `run.ps1` to start the application. Otherwise, read the two scripts to run the commands using Python.
   - Sets appropriate environment variables for colors, fonts, and display settings
     ng with VS Code
     To run the application:
     t make it easy to run Metrix:
1. Open the Debug panel in VS Code (Ctrl+Shift+D or click the debug icon in the sidebar)
1. Select "Python: Debug" from the dropdown at the topcation with a default configuration
1. Click the green play button or press F5 - Renders a standard Metrix GIF with GitHub user stats

For running test scripts and bulk generation tools, see the [tests documentation](src/tests/README.md).
application:

## Credits

Fonts by **VileR**: [Oldschool PC Fonts](https://int10h.org/oldschool-pc-fonts/fontlist/)2. Select "Python: Debug" from the dropdown at the top
he green play button or press F5

## License

e [tests documentation](src/tests/README.md).
This project is licensed under the [MIT License](LICENSE).

## Credits

Fonts by **VileR**: [Oldschool PC Fonts](https://int10h.org/oldschool-pc-fonts/fontlist/)

## License

This project is licensed under the [MIT License](LICENSE).
