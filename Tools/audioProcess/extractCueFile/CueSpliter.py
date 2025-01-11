
from ffcuesplitter.cuesplitter import FFCueSplitter
from ffcuesplitter.user_service import FileSystemOperations


class SplitRet:
    def __init__(self, isOk=True, errMsg="", data=None):
        self.isOk = isOk
        self.errMsg = errMsg
        self.data = data


class CueSpliter:
    def __core(cue_path, output_path, output_format="flac"):
        return FileSystemOperations(filename=cue_path, outputdir=output_path,
                                    outputformat=output_format, overwrite='always')

    """
    Type of return object is list(dict):
    [
      {
        "FILE": xxx,
        "ALBUM": xxx,
        "PERFORMER": xxx,
        "DATE": xxx,
        "GENRE": xxx,
        "DISCID": xxx,
        "COMMENT": xxx,
        "TITLE": xxx,
        "TRACK_NUM": xxx,
        "ISRC": xxx,
        "INDEX": xxx,
        "START": xxx,
        "END": xxx,
        "DURATION": xxx,
      }
    ]
    """
    def getCueInfo(cue_path):
        try:
            getdata = FFCueSplitter(filename=cue_path, dry=True)
            return SplitRet(True, "", getdata.audiotracks)
        except Exception as e:
            return SplitRet(False, str(e))

    def doSplit(cue_file, output_path):
        try:
            split = CueSpliter.__core(cue_file, output_path)
            if split.kwargs['dry']:
                split.dry_run_mode()
            else:
                overwr = split.check_for_overwriting()
                if not overwr:
                    split.work_on_temporary_directory()
        except Exception as e:
            return SplitRet(False, str(e))
        else:
            return SplitRet()


try:
    print(CueSpliter.getCueInfo("/Users/intro/Downloads/1.jpg"))
except Exception as e:
    print(e)
