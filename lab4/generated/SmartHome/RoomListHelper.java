//
// Copyright (c) ZeroC, Inc. All rights reserved.
//
//
// Ice version 3.7.10
//
// <auto-generated>
//
// Generated from file `smarthome.ice'
//
// Warning: do not edit this file.
//
// </auto-generated>
//

package SmartHome;

/**
 * Helper class for marshaling/unmarshaling RoomList.
 **/
public final class RoomListHelper
{
    public static void write(com.zeroc.Ice.OutputStream ostr, Room[] v)
    {
        if(v == null)
        {
            ostr.writeSize(0);
        }
        else
        {
            ostr.writeSize(v.length);
            for(int i0 = 0; i0 < v.length; i0++)
            {
                Room.ice_write(ostr, v[i0]);
            }
        }
    }

    public static Room[] read(com.zeroc.Ice.InputStream istr)
    {
        final Room[] v;
        final int len0 = istr.readAndCheckSeqSize(13);
        v = new Room[len0];
        for(int i0 = 0; i0 < len0; i0++)
        {
            v[i0] = Room.ice_read(istr);
        }
        return v;
    }

    public static void write(com.zeroc.Ice.OutputStream ostr, int tag, java.util.Optional<Room[]> v)
    {
        if(v != null && v.isPresent())
        {
            write(ostr, tag, v.get());
        }
    }

    public static void write(com.zeroc.Ice.OutputStream ostr, int tag, Room[] v)
    {
        if(ostr.writeOptional(tag, com.zeroc.Ice.OptionalFormat.FSize))
        {
            int pos = ostr.startSize();
            RoomListHelper.write(ostr, v);
            ostr.endSize(pos);
        }
    }

    public static java.util.Optional<Room[]> read(com.zeroc.Ice.InputStream istr, int tag)
    {
        if(istr.readOptional(tag, com.zeroc.Ice.OptionalFormat.FSize))
        {
            istr.skip(4);
            Room[] v;
            v = RoomListHelper.read(istr);
            return java.util.Optional.of(v);
        }
        else
        {
            return java.util.Optional.empty();
        }
    }
}
