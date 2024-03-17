import QtQuick 1.1
import com.victron.velib 1.0
import "utils.js" as Utils

MbPage {
    id: root
    property variant service

    property string bindPrefix: "com.victronenergy.settings"
	property string platformPrefix: "com.victronenergy.platform"

	model: VisibleItemModel {
		MbItemValue {
			description: qsTr("Firmware version")
			item.bind: Utils.path(platformPrefix, "/Firmware/Installed/Version")
		}

		MbItemValue {
			description: qsTr("Build date/time")
			item.bind: Utils.path(platformPrefix, "/Firmware/Installed/Build")
		}

		MbSubMenu {
			description: qsTr("Online updates")
			subpage: Component {
                PageSettingsFirmwareOnline {}
            }
		}

		MbSubMenu {
			description: qsTr("Install firmware from SD/USB")
			subpage: Component {
                PageSettingsFirmwareOffline {}
            }
		}

		MbSubMenu {
			description: qsTr("Stored backup firmware")
			subpage: Component {
				PageSettingsRootfsSelect {}
			}
		}

		MbSubMenu {
			description: qsTr("CPU Monitor")
			subpage: Component {
                PageSettingsCPU {}
            }
		}
	}
}
