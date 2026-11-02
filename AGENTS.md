# Repository Guidance

- Keep each skill self-contained under `skills/<skill-name>/`.
- Use lowercase hyphenated names and keep the directory name equal to the YAML `name`.
- Keep the entrypoint concise; link detailed references and optional assets where needed.
- Preserve the user's chosen environment and distinguish example values from requirements.
- Record the environment and scope of actual verification. Do not label unexecuted workflows as tested.
- Update the README index when adding or changing the purpose of a skill.
- Run `python scripts/validate_skills.py` and the validator's unit tests after relevant changes. Run changed examples in their target environment when practical.
- Use `feature/` branches and DCO-signed commits with `git commit -sm`.
- Treat the Git repository as the source of truth. Update installed skill copies only when requested.
