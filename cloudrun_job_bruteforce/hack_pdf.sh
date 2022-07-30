#!/bin/sh

pdf2john encrypted/report_6_chars.pdf >> hash/report_6_chars.txt
john hash/report_6_chars.txt --wordlist=dictionary.txt --progress-every=10 
