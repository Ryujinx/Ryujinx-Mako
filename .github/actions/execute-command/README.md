# execute-command

A small composite action to run the specified Mako subcommand.

## Usage

Add the following step to your workflow:

```yml
- name: Execute Ryujinx-Mako command
  uses: Ryujinx/Ryujinx-Mako/.github/actions/execute-command@master
  with:
    command: "<a valid subcommand for Mako>"
    args: "<subcommand args>"
    app_id: ${{ secrets.MAKO_APP_ID }}
    private_key: ${{ secrets.MAKO_PRIVATE_KEY }}
    installation_id: ${{ secrets.MAKO_INSTALLATION_ID }}
```


