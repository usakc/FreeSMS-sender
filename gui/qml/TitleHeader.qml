import QtQuick 1.1
import com.nokia.meego 1.0

Rectangle{
	property alias title: titleText.text
	id: headerRect
	anchors.top:mainPage.top; anchors.left: mainPage.left; anchors.right: mainPage.right
	width: mainPage.width ; 
	height: 80
	color: "transparent"
	Text {
		id: titleText
		anchors.centerIn: headerRect
		font.bold: true
		font.pointSize: 20
		text: qsTr("Free SMS")
	}
	Rectangle {
		x: 0; y: parent.height - 2
		width: parent.width
		height: 1
		color: "gray"
		opacity: 0.6
	}
}
