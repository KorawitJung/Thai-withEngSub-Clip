# Thai-withEngSub-Clip

A Claude Code skill for making vertical animated clips in Thai, English, or both languages in one clip, from script, voiceover, subtitles, and visuals through to the final MP4.

- **Languages:** Thai, English, bilingual subtitles, mixed-language narration, or separate versions for each language
- **Styles:** `story-night`, `story-warm`, `horror-rules`, `explainer-paper`, `data-clean`
- **Genres:** suspense, horror, folklore, step-by-step tutorials, business explainers, news briefs, and local promos

## Installation
Download the repo:
```bash
git clone https://github.com/KorawitJung/Thai-withEngSub-Clip.git
```
Then copy the `skills/thai-withengsub-clip` folder to `~/.claude/skills/thai-withengsub-clip` (on Windows, `%USERPROFILE%\.claude\skills\thai-withengsub-clip`) and start a new session.

On Mac or Linux:
```bash
mkdir -p ~/.claude/skills && cp -R Thai-withEngSub-Clip/skills/thai-withengsub-clip ~/.claude/skills/
```

On Windows PowerShell:
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null; Copy-Item -Recurse -Force "Thai-withEngSub-Clip\skills\thai-withengsub-clip" "$env:USERPROFILE\.claude\skills\"
```

You need Python 3.10+, ffmpeg, Node.js, and an ElevenLabs key for real voiceovers. To generate music locally, you also need uv and about 4 GB of disk space.

## Usage
Open your project folder in Claude Code, then run `/thai-withengsub-clip` or type a request in Thai or English, such as:
- `Make a clip about a ghost story from Isan with Thai narration and Thai and English subtitles`
- `Make an English explainer reel about why short videos lose viewers`
- `Turn this news story into a 45-second clip with separate Thai and English versions`
- `Suggest 5 reel ideas based on teen trends, then make one into a fun clip with characters and memes`

For clips with many characters, memes, and animated charts, see the Remotion template in `skills/thai-withengsub-clip/examples/remotion-reel`.

## Costs
- ElevenLabs charges by character. Run `narrate.py --dry-run` to see the count before generating a voiceover, then compare it with your plan on the provider's website, because quotas, prices, and commercial rights can change.
- The other steps in the skill have no service fee, but check the licenses for fonts, Openverse sounds, and music models. The default model in `music.py` does not allow commercial use.

## Troubleshooting
| Problem | Fix |
|---|---|
| A program is missing | Run `check_env.py`, then install what is missing by following `references/tools.md` |
| Subtitles don't match the voice | Check that `say` matches `narration.txt`, and use the alignment file from the same audio set |
| The voiceover is too long | Cut the script, or use `tighten.py` |
| Music takes a long time to load | This is normal the first time, or use `soundscape.py` instead |

## Testing
```bash
python -m unittest discover -s tests
```

## License
MIT. See `LICENSE`, and see `THIRD_PARTY.md` for the external services used.
