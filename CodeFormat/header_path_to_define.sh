# use for goole open source code format
#
# Usage: 
#   user$ ./header_path_to_define.sh temp/header.h
#   TEMP_HEADER_H_

echo "$1_" | tr 'a-z' 'A-Z' | sed -e 's/\//_/g' -e s'/\./_/'

