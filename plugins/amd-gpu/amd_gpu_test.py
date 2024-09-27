#!/usr/bin/env python3
#
# Copyright 2024 Mario Limonciello <mario.limonciello@amd.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import gi
import os
import sys
import unittest
from fwupd_test import FwupdTest, override_gi_search_path

gi.require_version("UMockdev", "1.0")
from gi.repository import UMockdev

try:
    override_gi_search_path()
    gi.require_version("Fwupd", "2.0")
    from gi.repository import Fwupd  # pylint: disable=wrong-import-position
except ValueError:
    # when called from unittest-inspector this might not pass, we'll fail later
    # anyway in actual use
    pass

try:
    from amd_gpu_ioctl import handle_ioctl
except ImportError:
    # when called from unittest-inspector this might not pass, we'll fail later
    # anyway in actual use
    pass


class AmdGpuApuTest(FwupdTest):
    def setUp(self):
        super().setUp()
        self.testbed.add_from_string(
            """P: /devices/pci0000:00/0000:00:08.1/0000:c1:00.0/drm/card0
N: dri/card0
S: dri/by-path/pci-0000:c1:00.0-card
E: DEVLINKS=/dev/dri/by-path/pci-0000:c1:00.0-card
E: DEVNAME=/dev/dri/card0
E: DEVTYPE=drm_minor
E: ID_FOR_SEAT=drm-pci-0000_c1_00_0
E: ID_PATH=pci-0000:c1:00.0
E: ID_PATH_TAG=pci-0000_c1_00_0
E: MAJOR=226
E: MINOR=0
E: SUBSYSTEM=drm
A: dev=226:0
L: device=../../../0000:c1:00.0
"""
        )
        self.testbed.add_from_string(
            """P: /devices/pci0000:00/0000:00:08.1/0000:c1:00.0
E: DRIVER=amdgpu
E: ID_MODEL_FROM_DATABASE=Phoenix1
E: ID_PATH=pci-0000:c1:00.0
E: ID_PATH_TAG=pci-0000_c1_00_0
E: ID_PCI_CLASS_FROM_DATABASE=Display controller
E: ID_PCI_INTERFACE_FROM_DATABASE=VGA controller
E: ID_PCI_SUBCLASS_FROM_DATABASE=VGA compatible controller
E: ID_VENDOR_FROM_DATABASE=Advanced Micro Devices, Inc. [AMD/ATI]
E: MODALIAS=pci:v00001002d000015BFsv0000F111sd00000006bc03sc00i00
E: NVME_HOST_IFACE=none
E: PCI_CLASS=30000
E: PCI_ID=1002:15BF
E: PCI_SLOT_NAME=0000:c1:00.0
E: PCI_SUBSYS_ID=F111:0006
E: SUBSYSTEM=pci
A: apu_thermal_cap=failed to get thermal limit
A: ari_enabled=0
A: boot_vga=1
A: broken_parity_status=0
A: class=0x030000
H: config=0210BF1507041000CB000003100080000C000000780000000C0000900000000001100000000050900000000011F10600000000004800000000000000FF010000
A: consistent_dma_mask_bits=44
L: consumer:pci:0000:c1:00.1=../../../virtual/devlink/pci:0000:c1:00.0--pci:0000:c1:00.1
A: current_link_speed=16.0 GT/s PCIe
A: current_link_width=16
A: d3cold_allowed=1
A: device=0x15bf
A: dma_mask_bits=44
L: driver=../../../../bus/pci/drivers/amdgpu
A: driver_override=(null)
L: drm/controlD64=card0
A: enable=1
L: firmware_node=../../../LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/device:16/LNXVIDEO:00
A: fw_version/asd_fw_version=0x210000c7
A: fw_version/ce_fw_version=0x00000000
A: fw_version/dmcu_fw_version=0x00000000
A: fw_version/imu_fw_version=0x0b012d00
A: fw_version/mc_fw_version=0x00000000
A: fw_version/me_fw_version=0x00000027
A: fw_version/mec2_fw_version=0x00000000
A: fw_version/mec_fw_version=0x00000023
A: fw_version/mes_fw_version=0x00000052
A: fw_version/mes_kiq_fw_version=0x00000073
A: fw_version/pfp_fw_version=0x0000002f
A: fw_version/rlc_fw_version=0x0000007f
A: fw_version/rlc_srlc_fw_version=0x00000000
A: fw_version/rlc_srlg_fw_version=0x00000000
A: fw_version/rlc_srls_fw_version=0x00000000
A: fw_version/sdma2_fw_version=0x00000000
A: fw_version/sdma_fw_version=0x00000010
A: fw_version/smc_fw_version=0x004c4e00
A: fw_version/sos_fw_version=0x00000000
A: fw_version/ta_ras_fw_version=0x00000000
A: fw_version/ta_xgmi_fw_version=0x00000000
A: fw_version/uvd_fw_version=0x00000000
A: fw_version/vce_fw_version=0x00000000
A: fw_version/vcn_fw_version=0x0510c000
A: gpu_busy_percent=3
H: gpu_metrics=780002016810E5100000A00F0000DE0F8D101D10B31042105B10FFFF60010000DC4A58DB9C4300002A13FFFFE903F20A0000030000000005760803000300030020039001E803E80320032003FFFFFFFFFFFFFFFFFFFFFFFF0000780500004E0C4E0C4E0C780578054E0CFFFF00000000FFFFFFFFFFFFFFFF
H: hdcp_srm=800000010000002BD2489E49D057AE315B1ABCE00E4F6B92A6BA033B98CCED4A978F5DD227292519A5D5F05D5E563D0E
A: link/l0s_aspm=0
A: link/l1_aspm=0
A: local_cpulist=0-11
A: local_cpus=0fff
A: max_link_speed=16.0 GT/s PCIe
A: max_link_width=16
A: mem_info_gtt_total=3796545536
A: mem_info_gtt_used=869117952
A: mem_info_preempt_used=0
A: mem_info_vis_vram_total=536870912
A: mem_info_vis_vram_used=489570304
A: mem_info_vram_total=536870912
A: mem_info_vram_used=489570304
A: mem_info_vram_vendor=unknown
A: modalias=pci:v00001002d000015BFsv0000F111sd00000006bc03sc00i00
A: pcie_replay_count=0
A: power_dpm_force_performance_level=auto
A: power_dpm_state=performance
A: power_state=D0
A: pp_cur_state=0
A: pp_dpm_dcefclk=
A: pp_dpm_fclk=0: 500Mhz *1: 1400Mhz 2: 1600Mhz 3: 1960Mhz
A: pp_dpm_mclk=0: 1000Mhz *1: 2800Mhz 2: 1600Mhz 3: 2800Mhz
A: pp_dpm_pcie=
A: pp_dpm_sclk=0: 800Mhz *1: 1100Mhz 2: 2599Mhz
A: pp_dpm_socclk=0: 400Mhz *1: 600Mhz 2: 720Mhz 3: 800Mhz 4: 900Mhz 5: 1028Mhz 6: 1028Mhz 7: 1200Mhz
A: pp_force_state=
A: pp_mclk_od=0
A: pp_num_states=states: 10 default
H: pp_od_clk_voltage=4F445F53434C4B3A0A303A20202020202020203830304D687A0A313A20202020202020323539394D687A0A000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004F445F52414E47453A0A53434C4B3A20202020203830304D687A20202020202020323539394D687A0A0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
A: pp_sclk_od=0
A: reset_method=bus
A: resource=0x0000007800000000 0x000000780fffffff 0x000000000014220c0x0000000000000000 0x0000000000000000 0x00000000000000000x0000000090000000 0x00000000901fffff 0x000000000014220c0x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000001000 0x00000000000010ff 0x00000000000401010x0000000090500000 0x000000009057ffff 0x00000000000402000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x0000000000000000
A: revision=0xcb
A: subsystem_device=0x0006
A: subsystem_vendor=0xf111
A: thermal_throttling_logging=0000:c1:00.0: thermal throttling logging enabled, with interval 60 seconds
A: unique_id=
A: vbios_version=113-PHXGENERIC-001
A: vendor=0x1002
"""
        )
        self.testbed.add_from_string(
            """P: /devices/pci0000:00/0000:00:08.1
E: DRIVER=pcieport
E: ID_PATH=pci-0000:00:08.1
E: ID_PATH_TAG=pci-0000_00_08_1
E: ID_PCI_CLASS_FROM_DATABASE=Bridge
E: ID_PCI_INTERFACE_FROM_DATABASE=Normal decode
E: ID_PCI_SUBCLASS_FROM_DATABASE=PCI bridge
E: ID_VENDOR_FROM_DATABASE=Advanced Micro Devices, Inc. [AMD]
E: MODALIAS=pci:v00001022d000014EBsv00000006sd0000F111bc06sc04i00
E: PCI_CLASS=60400
E: PCI_ID=1022:14EB
E: PCI_SLOT_NAME=0000:00:08.1
E: PCI_SUBSYS_ID=0006:F111
E: SUBSYSTEM=pci
A: ari_enabled=0
A: broken_parity_status=0
A: class=0x060400
H: config=2210EB14070410000000040610008100000000000000000000C1C1001111000000905090010071107800000078000000000000005000000000000000FF010200
A: consistent_dma_mask_bits=32
A: current_link_speed=16.0 GT/s PCIe
A: current_link_width=16
A: d3cold_allowed=1
A: device=0x14eb
A: dma_mask_bits=32
L: driver=../../../bus/pci/drivers/pcieport
A: driver_override=(null)
A: enable=2
A: max_link_speed=16.0 GT/s PCIe
A: max_link_width=16
A: modalias=pci:v00001022d000014EBsv00000006sd0000F111bc06sc04i00
A: power_state=D0
A: reset_method=pm
A: resource=0x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000000000 0x0000000000000000 0x00000000000000000x0000000000001000 0x0000000000001fff 0x00000000000001010x0000000090000000 0x00000000905fffff 0x00000000000002000x0000007800000000 0x00000078107fffff 0x00000000001022010x0000000000000000 0x0000000000000000 0x0000000000000000
A: revision=0x00
A: secondary_bus_number=193
A: subordinate_bus_number=193
A: subsystem_device=0xf111
A: subsystem_vendor=0x0006
A: vendor=0x1022
"""
        )
        # handler for the IOCTL
        handler = UMockdev.IoctlBase()
        handler.connect("handle-ioctl", handle_ioctl)
        self.testbed.attach_ioctl("/dev/dri/card0", handler)

    def tearDown(self):
        self.testbed.detach_ioctl("/dev/dri/card0")
        super().tearDown()

    def test_apu_device(self):
        self.start_daemon()
        devices = Fwupd.Client().get_devices()

        count = 0
        for dev in devices:
            if dev.get_plugin() != "amd_gpu":
                continue
            print(dev.to_string())
            count += 1
            self.assertEqual(
                dev.get_flags(),
                1 | Fwupd.DeviceFlags.INTERNAL,
            )
            self.assertEqual(dev.get_summary(), "AMD AMD_PHOENIX_GENERIC")
            self.assertEqual(dev.get_vendor(), "Advanced Micro Devices, Inc. [AMD/ATI]")
            self.assertEqual(dev.get_version(), "022.012.000.027.000001")
            guids = dev.get_guids()
            self.assertEqual(len(guids), 1)
            self.assertIn("4a1501b7-b500-5255-9d9c-41d652a4d5bc", guids)
            instance_ids = dev.get_instance_ids()
            self.assertEqual(len(instance_ids), 1)
            self.assertIn("AMD\\113-PHXGEN", instance_ids)
        self.assertGreater(count, 0)


if __name__ == "__main__":
    # run ourselves under umockdev
    if "umockdev" not in os.environ.get("LD_PRELOAD", ""):
        os.execvp("umockdev-wrapper", ["umockdev-wrapper", sys.executable] + sys.argv)

    prog = unittest.main(exit=False)
    if prog.result.errors or prog.result.failures:
        sys.exit(1)

    # Translate to skip error
    if prog.result.testsRun == len(prog.result.skipped):
        sys.exit(77)
