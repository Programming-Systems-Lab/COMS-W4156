Install Git, Google Cloud SDK, Python 2.7, Pip, Ruby, Ruby libraries, Virtualenv (optional), Curl

#### Install virtual machine (Optional)
We recommend installing Linux (Ubuntu) and using it for local development.  The principal motivation is to ensure library and application compatibility with your continuous integration and deployment (Travis and Google App Engine) chain.  Travis runs Ubuntu 14.04.  If you have to do something special in your environment, then you will need to do it on deployment.  We especially recommend this if your team has a mixture of Macs and Windows or just Windows machines.  Diligent use of `virtualenv` can overcome library issues on Macs and Linux machines.

There are some side benefits as well, namely, you can destroy and rebuild the VM without affecting the rest of your computer.  One of the authors has still not removed all unnecessary libraries and tools.

1. Download and install VirtualBox, [https://www.virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads).
2. Download the desktop version of [Ubuntu 16.04](http://releases.ubuntu.com/16.04/).  Alternatively, you can choose Xubuntu, which has a different lighter-weight interface, from [Xubuntu 16.04](http://mirror.us.leaseweb.net/ubuntu-cdimage/xubuntu/releases/16.04/release/xubuntu-16.04.2-desktop-amd64.iso).  If you have a 32-bit machine use this link: [http://mirror.us.leaseweb.net/ubuntu-cdimage/xubuntu/releases/16.04/release/xubuntu-16.04.2-desktop-i386.iso](http://mirror.us.leaseweb.net/ubuntu-cdimage/xubuntu/releases/16.04/release/xubuntu-16.04.2-desktop-i386.iso)  Xubuntu is full compatible with Ubuntu 16.04.
3. Run VirtualBox and create a New Machine.  Give the machine a name (e.g. 4156), select Linux.  Select how much memory (generally half your machines memory is a good choice) and create a virtual disk image (recommend dynamically allocated with 20 GB maximum).
4. Setup your VirtualBox (Number of CPUs, video memory, acceleration).  I just choose the things that seem the best and let it complain if the settings are bad.
5. Start the virtual machine, you will be asked for a .iso and point it to the Ubuntu image you just downloaded.  the default selections are fine.
> Note: Some Windows laptop manufacturers turn off Virtualization (you'll get a cryptic error about "VT-x") by default.  You will need to enter your BIOS to turn it on.  They can also permanently disable it as well, although few seem to do this.  If it is permanently disabled then install the tools on your Window machine or dual boot.
6. You will probably get a warning about "auto-capture" of you mouse and keyboard.  That is fine, it means that if you mouse over the VM or if the VM is the foreground application mouse and keyboard inputs will got to the VM.
7. Once you are in Ubuntu, you want to update it, `sudo apt update && sudo apt upgrade`.
8. Install VirtualBox additions and turn on Shared Clipboard (`Devices > Shared Clipboard > Bidirectional`).  Verify you copy and paste from the host to the virtual machine.  You'll need to reboot the VM to get additions to run correctly (you may need to reboot the host as well.)  In a terminal ctrl-shift-c and ctrl-shift-v are copy and paste.

    `sudo apt install virtualbox-guest-dkms`

Additional Installation Material is [here](https://linus.nci.nih.gov/bdge/installUbuntu.html).

#### Install Local Files (Ubuntu Commands)
Install Git, Pip, Virtualenv, Ruby, [Google Cloud SDK](https://cloud.google.com/sdk/docs/#deb)

    sudo apt-get install git python-pip ruby ruby-dev curl xclip
    sudo -H pip install --upgrade pip
    sudo -H pip install virtualenv
    # The following is to install Google SDK    
    export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
    echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    sudo apt-get update && sudo apt-get install google-cloud-sdk

#### Important note:
If you host machine goes to sleep, it may corrupt the virtual machine's drive.  Always save File > Close > Save or power off the virtual machine before putting your computer to sleep.
