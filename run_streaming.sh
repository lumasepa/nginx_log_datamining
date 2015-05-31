#!/usr/bin/env bash

MAPPER="mapper.py"
REDUCER="reducer.py"
INPUT=""
OUTPUT=""
TEST=""

while (( $# )); do

	case $1 in

	-i|–input )
		shift
		INPUT="$INPUT -input $1"
	;;
	-ip|–input-pattern )
		shift
		INPUT_PATTERN="$1"
	;;
	-o|-output )
		shift
		OUTPUT=$1
	;;
	-m|-mapper )
		shift
		MAPPER=$1
	;;
	-r|-reducer )
		shift
		REDUCER=$1
	;;
	-t|-test )
		TEST="TRUE"
	;;
	--help )
		echo "$0 [-m|-mapper MAPPER] [-r|-reducer REDUCER] [-o|-output OUTPUTDIR] [-i|-input INPUTFILE(s)] [-t|-test]"
		echo "Por defecto el mapper es mapper.py y el reducer es reducer.py"
		echo "-output y -input son necesarios"
		echo "En el caso de indicar -test no se usa hadoop, sino se corre localmente para pruebas"
		exit
	;;
	* )
		echo "$1 Parametro incorrecto --help para ayuda"
		exit
	;;
	esac
	shift
done

if [ -z "$INPUT" ] && [ -z "$INPUT_PATTERN" ]
then
    echo "Necesario parametro -input o -input-pattern"
fi

if [ "$INPUT_PATTERN" ]
then
	INPUT_PATTERN_FILES="$(for i in `find . -name $INPUT_PATTERN`; do FILES="$FILES -input $i"; done; echo $FILES)"
else
	INPUT_PATTERN_FILES=""
fi


if [ -z "$TEST" ]
then

    if [ -z "$OUTPUT" ]
    then
        echo "Necesario parametro -output"
    fi

    FILES="$(for i in `find . -name "*.py"`; do FILES="$FILES -file $i"; done; echo $FILES)"

    ../bin/hadoop jar ../share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar $INPUT_PATTERN_FILES $FILES -mapper $MAPPER -reducer $REDUCER $INPUT -output $OUTPUT
else
    cat "./$(echo "$INPUT $INPUT_PATTERN_FILES" | sed "s/-input//g" | sed "s/ //g")" | ./$MAPPER | sort | ./$REDUCER
fi

