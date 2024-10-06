import QtQuick 1.1
import com.victron.velib 1.0
import "utils.js" as Utils


MbPage {
    property variant service
    property string cpuPrefix: "com.victronenergy.cpu"

    title: "CPU Monitor"

	model: VisibleItemModel {

        MbItemValue {
            description: qsTr("CPU Load Overall")
            item {
                bind: Utils.path(cpuPrefix, "/CPU_Load")
                unit: "%"
                decimals: 1
            }
        }
        MbItemValue {
            description: qsTr("CPU Load User")
            item {
                bind: Utils.path(cpuPrefix, "/CPU_Load_User")
                unit: "%"
                decimals: 1
            }
        }
        MbItemValue {
            description: qsTr("CPU Load System")
            item {
                bind: Utils.path(cpuPrefix, "/CPU_Load_System")
                unit: "%"
                decimals: 1
            }
        }
        MbItemValue {
            description: qsTr("CPU Memory Free")
            item {
                bind: Utils.path(cpuPrefix, "/CPU_Memory_Free")
                unit: "MB"
                decimals: 0
            }
        }
        MbItemValue {
            description: qsTr("CPU Top 1 Min")
            item {
                bind: Utils.path(cpuPrefix, "/CPU_AVG_1")
                decimals: 2
            }
        }
        MbItemValue {
            description: qsTr("CPU Top 5 Min")
            item {
                bind: Utils.path(cpuPrefix, "/CPU_AVG_5")
                decimals: 2
            }
        }
        MbItemValue {
            description: qsTr("CPU Top 15 Min")
            item {
                bind: Utils.path(cpuPrefix, "/CPU_AVG_15")
                decimals: 2
            }
        }
        MbItemValue {
            description: qsTr("CPU Memory Used")
            item {
                bind: Utils.path(cpuPrefix, "/CPU_Memory_Used")
                unit: "MB"
                decimals: 0
            }
        }
        MbItemValue {
            description: qsTr("CPU Memory Buffers")
            item {
                bind: Utils.path(cpuPrefix, "/CPU_Memory_Buffers")
                unit: "MB"
                decimals: 0
            }
        }
    }
}

