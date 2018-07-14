# Useful Linux Commands

* df - df displays the amount of disk space available on the file system containing each file name argument.

* du -sh $folderName - estimate file space usage

* ldd - print shared object dependencies

* cat /etc/lsb-release - get distibution info

* lscpu - display information about the CPU architecture

* lspci - list all PCI devices

* sudo lshw -C display - display GPU info

* diff -y --suppress-common-lines file1 file2 | aha --black --title 'report-diff' > reportDiff.html

* lsmod | grep kfd - - Show the status of modules in the Linux Kernel

* lsb_release -a for information related to the Ubuntu version

* uname -r

* 2>&1 | tee output.log - save error & output stream

* sudo chmod -R a+wrX folder - write permission