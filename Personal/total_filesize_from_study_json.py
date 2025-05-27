# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 09:17:17 2025

@author: Subin-PC
"""

import json

# Replace this with loading from a file if 
'''
 when the JSON is serialized, Python's boolean values True and False are converted to JSON's boolean values 
 true and false (lowercase). When we read the JSON back, these values stay lowercase. So manually replaced "false" for 
 "is_multiframe" key to "False"
'''
data = {
    "instances": [
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000294",
                        "file_info": {
                            "filesize": 211232
                        },
                        "offset_info": {
                            "pixel_data_offset": 112540,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000296",
                        "file_info": {
                            "filesize": 211248
                        },
                        "offset_info": {
                            "pixel_data_offset": 112542,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000297",
                        "file_info": {
                            "filesize": 211146
                        },
                        "offset_info": {
                            "pixel_data_offset": 112540,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000298",
                        "file_info": {
                            "filesize": 210964
                        },
                        "offset_info": {
                            "pixel_data_offset": 112540,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000299",
                        "file_info": {
                            "filesize": 211052
                        },
                        "offset_info": {
                            "pixel_data_offset": 112542,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000300",
                        "file_info": {
                            "filesize": 211224
                        },
                        "offset_info": {
                            "pixel_data_offset": 112542,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000301",
                        "file_info": {
                            "filesize": 211246
                        },
                        "offset_info": {
                            "pixel_data_offset": 112540,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000302",
                        "file_info": {
                            "filesize": 211144
                        },
                        "offset_info": {
                            "pixel_data_offset": 112540,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000303",
                        "file_info": {
                            "filesize": 211074
                        },
                        "offset_info": {
                            "pixel_data_offset": 112540,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000304",
                        "file_info": {
                            "filesize": 211210
                        },
                        "offset_info": {
                            "pixel_data_offset": 112548,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000305",
                        "file_info": {
                            "filesize": 211194
                        },
                        "offset_info": {
                            "pixel_data_offset": 112548,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000306",
                        "file_info": {
                            "filesize": 211040
                        },
                        "offset_info": {
                            "pixel_data_offset": 112548,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000307",
                        "file_info": {
                            "filesize": 211086
                        },
                        "offset_info": {
                            "pixel_data_offset": 112548,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000308",
                        "file_info": {
                            "filesize": 211090
                        },
                        "offset_info": {
                            "pixel_data_offset": 112548,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000309",
                        "file_info": {
                            "filesize": 211180
                        },
                        "offset_info": {
                            "pixel_data_offset": 112548,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000310",
                        "file_info": {
                            "filesize": 211024
                        },
                        "offset_info": {
                            "pixel_data_offset": 112548,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    },
                    {
                        "SOPInstanceUID": "1.3.12.2.1107.5.2.30.59097.30000017021009063092200000311",
                        "file_info": {
                            "filesize": 211236
                        },
                        "offset_info": {
                            "pixel_data_offset": 112548,
                            "first_16_bytes_hex": "e07f10004f570000fffffffffeff00e0",
                            "transfer_syntax_uid": "1.2.840.10008.1.2.4.90",
                            "is_multiframe": False
                        }
                    }
                ]
            }


# Calculate total filesize
total_filesize = sum(instance["file_info"]["filesize"] for instance in data["instances"])
total_gb = total_filesize / (1024 ** 3)

print("Total filesize:", total_filesize)
print("Total filesize in GB:", round(total_gb, 6))  # Round to 4 decimal places
