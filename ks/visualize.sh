#!/bin/bash
sort | awk '{ printf( "%d ", $3); if ( (NR % 9) == 0) printf( "\n" ); }'
