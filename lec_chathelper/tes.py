vcard = '<vCard xmlns="vcard-temp"><JABBERID>321@localhost</JABBERID><NICKNAME>Vu dep trai</NICKNAME><PHOTO><EXTVAL>https://bountycdn.azureedge.net/~/media/b9bedc08353044c5b7e354858f0c4db1.ashx?la=en</EXTVAL></PHOTO><PHOTO><EXTVAL>https://bountycdn.azureedge.net/~/media/b9bedc08353044c5b7e354858f0c4db1.ashx?la=en</EXTVAL></PHOTO></vCard>'

from lxml import etree
root = etree.XML('<vCard xmlns="vcard-temp"><JABBERID>321@localhost</JABBERID><NICKNAME>Vu dep trai</NICKNAME><PHOTO><EXTVAL>https://bountycdn.azureedge.net/~/media/b9bedc08353044c5b7e354858f0c4db1.ashx?la=en</EXTVAL></PHOTO><PHOTO><EXTVAL>https://bountycdn.azureedge.net/~/media/b9bedc08353044c5b7e354858f0c4db1.ashx?la=vi</EXTVAL></PHOTO></vCard>')

hello = root.find("vcard-temp/JABBERDID")