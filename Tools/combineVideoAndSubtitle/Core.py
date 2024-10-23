import os
import sys
import tkinter as tk
import subprocess
import time


# reference https://www.cnblogs.com/chenqionghe/p/11532245.html
def run_shell(shell):
    cmd = subprocess.Popen(
        shell,
        stdin=subprocess.PIPE,
        stderr=sys.stderr,
        close_fds=True,
        stdout=sys.stdout,
        universal_newlines=True,
        shell=True,
        bufsize=1,
    )
    cmd.communicate()
    return cmd.returncode


def getStrFromBytes(bytes):
    line = ""
    system_encoding = sys.getdefaultencoding()
    try:
        line = bytes.decode(system_encoding)
    except:
        print('getStrFromBytes unsupport %s' % (system_encoding))

    return line


def printMsgToTextBox(msg, textBox):
    textBox.config(state=tk.NORMAL)
    textBox.insert(tk.END, msg)
    textBox.see(tk.END)
    textBox.config(state=tk.DISABLED)


def core(videoFiles, subtitleFiles, aimAddress, msgTextBox, finishCb=None):
    src_path = videoFiles
    sub_path = subtitleFiles

    out_folder = aimAddress

    if not os.path.exists(out_folder):
        printMsgToTextBox(
            "Folder %s not find, folder will be create" % (
                out_folder), msgTextBox
        )
        os.mkdir(out_folder)

    ffmpeg = ""
    cmd_str = ""

    if sys.platform == "win32":
        ffmpeg = "ffmpeg.exe"
    elif sys.platform == "darwin":
        ffmpeg = "ffmpeg"

    for i in range(0, len(src_path)):
        if ffmpeg == "":
            break
        out_path = out_folder + os.sep + os.path.split(src_path[i])[-1]
        if os.path.exists(out_path):
            printMsgToTextBox(
                "File{%s} already exists, will be covered!\n" % (out_path),
                msgTextBox,
            )
            os.remove(out_path)
        cmd_str = (ffmpeg +
                    ' -i ' + '"%s"' % (src_path[i]) +
                    ' -i ' + '"%s"' % (sub_path[i]) +
                    ' -c ' + ' copy ' +
                    '"%s"' % (out_path))

        p = subprocess.Popen(
            cmd_str, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
        )
        printMsgToTextBox(
            "start combine: \n\tvideo file: %s\n\tsubtitle file: %s\n\tsave path: %s\n\twaiting...\n"
            % (src_path[i], sub_path[i], out_path),
            msgTextBox,
        )
        isError = False
        while True:
            output = None
            errOutput = None
            line = ""
            errorLine = ""
            if p.stdout:
                output = p.stdout.readline()
                line = getStrFromBytes(output)
            if p.stderr:
                errOutput = p.stderr.readline()
                errorLine = getStrFromBytes(errOutput)
                if errorLine != "":
                    printMsgToTextBox(errorLine, msgTextBox)
                    isError = True
            if (line == "" or errorLine != "") and p.poll() is not None:
                break
            else:
                print(line)
        if isError:
            printMsgToTextBox("Combine failed!\n", msgTextBox)
        else:
            printMsgToTextBox(
                "Combine Success, file is saved in %s!\n" % (
                    out_path), msgTextBox
            )

    if finishCb:
        finishCb()
