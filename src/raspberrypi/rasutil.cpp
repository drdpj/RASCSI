//---------------------------------------------------------------------------
//
//	SCSI Target Emulator RaSCSI (*^..^*)
//	for Raspberry Pi
//
//	Powered by XM6 TypeG Technology.
//	Copyright (C) 2016-2020 GIMONS
//  Copyright (C) 2020 akuker
//
//---------------------------------------------------------------------------

#include <unistd.h>
#include <sstream>
#include "rascsi_interface.pb.h"
#include "exceptions.h"
#include "rasutil.h"

using namespace std;
using namespace rascsi_interface;

//---------------------------------------------------------------------------
//
//	Serialize/Deserialize protobuf message: Length followed by the actual data
//
//---------------------------------------------------------------------------

void SerializeMessage(int fd, const google::protobuf::MessageLite& message)
{
	string data;
	message.SerializeToString(&data);

	// Write the size of the protobuf data as a header
    int32_t size = data.length();
    if (write(fd, &size, sizeof(size)) != sizeof(size)) {
    	throw ioexception("Can't write protobuf header");
    }

    // Write the actual protobuf data
    void *buf = malloc(size);
    memcpy(buf, data.data(), size);
    if (write(fd, buf, size) != size) {
    	free(buf);

    	throw ioexception("Can't write protobuf data");
    }

    free(buf);
}

void DeserializeMessage(int fd, google::protobuf::MessageLite& message)
{
	// First read the header with the size of the protobuf data
	int32_t size;
	if (read(fd, &size, sizeof(size)) == sizeof(size)) {
		// Read the actual protobuf data
		void *buf = malloc(size);
		if (read(fd, buf, size) != (ssize_t)size) {
			free(buf);

			throw ioexception("Missing protobuf data");
		}

		// Read protobuf data into a string, to be converted into a protobuf data structure by the caller
		string data((const char *)buf, size);
		free(buf);

		message.ParseFromString(data);
	}
}

//---------------------------------------------------------------------------
//
//	List devices
//
//---------------------------------------------------------------------------
string ListDevices(const PbDevices& devices) {
	ostringstream s;

	if (devices.devices_size()) {
    	s << endl
    		<< "+----+----+------+-------------------------------------" << endl
    		<< "| ID | UN | TYPE | DEVICE STATUS" << endl
			<< "+----+----+------+-------------------------------------" << endl;
	}
	else {
		return "No images currently attached.\n";
	}

	for (int i = 0; i < devices.devices_size() ; i++) {
		PbDevice device = devices.devices(i);

		s << "|  " << device.id() << " |  " << device.un() << " | " << device.type() << " | "
				<< device.file() << (device.read_only() ? " (WRITEPROTECT)" : "") << endl;
	}

	s << "+----+----+------+-------------------------------------" << endl;

	return s.str();
}