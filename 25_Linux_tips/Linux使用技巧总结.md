# Linux使用技巧总结

# 自定义命令行缩写

我们经常使用的一些Linux命令可以自定义一些缩写规则，提高效率。比如`ll` 代表 `ls -alF` ，我们可以通过往 `.bashrc` 文件中添加一些规则来实现该功能，`.bashrc` 文件位于Linux系统的home目录下，可以使用此命令打开：`vim ~/.bashrc`，可以在该文件中发现现有的一些命令缩写：

```bash
# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
```

比如我经常使用gedit编辑器，每次打开一个文件都要这样操作：`gedit test.txt`，现在我可以往 `.bashrc` 文件中添加这样一条规则： `alias g='gedit'`，将 `gedit`简化成 `g`，这样打开一个文件就可以这样操作了：`g test.txt`。需要注意的是，修改了 `.bashrc`文件后，需要重启当前终端才会生效。