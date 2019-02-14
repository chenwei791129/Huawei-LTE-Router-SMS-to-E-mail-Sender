#!/bin/sh
rm ./locale/zh_CN/LC_MESSAGES/messages.mo
msgfmt -o ./locale/zh_CN/LC_MESSAGES/messages.mo ./locale/zh_CN/LC_MESSAGES/messages.pot

rm ./locale/zh_TW/LC_MESSAGES/messages.mo
msgfmt -o ./locale/zh_TW/LC_MESSAGES/messages.mo ./locale/zh_TW/LC_MESSAGES/messages.pot

rm ./locale/zh_HK/LC_MESSAGES/messages.mo
msgfmt -o ./locale/zh_HK/LC_MESSAGES/messages.mo ./locale/zh_HK/LC_MESSAGES/messages.pot

rm ./locale/en_US/LC_MESSAGES/messages.mo
msgfmt -o ./locale/en_US/LC_MESSAGES/messages.mo ./locale/en_US/LC_MESSAGES/messages.pot

rm ./locale/en/LC_MESSAGES/messages.mo
msgfmt -o ./locale/en/LC_MESSAGES/messages.mo ./locale/en/LC_MESSAGES/messages.pot
