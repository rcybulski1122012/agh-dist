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
 * Helper class for marshaling/unmarshaling CleaningScheduleList.
 **/
public final class CleaningScheduleListHelper
{
    public static void write(com.zeroc.Ice.OutputStream ostr, CleaningSchedule[] v)
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
                CleaningSchedule.ice_write(ostr, v[i0]);
            }
        }
    }

    public static CleaningSchedule[] read(com.zeroc.Ice.InputStream istr)
    {
        final CleaningSchedule[] v;
        final int len0 = istr.readAndCheckSeqSize(37);
        v = new CleaningSchedule[len0];
        for(int i0 = 0; i0 < len0; i0++)
        {
            v[i0] = CleaningSchedule.ice_read(istr);
        }
        return v;
    }

    public static void write(com.zeroc.Ice.OutputStream ostr, int tag, java.util.Optional<CleaningSchedule[]> v)
    {
        if(v != null && v.isPresent())
        {
            write(ostr, tag, v.get());
        }
    }

    public static void write(com.zeroc.Ice.OutputStream ostr, int tag, CleaningSchedule[] v)
    {
        if(ostr.writeOptional(tag, com.zeroc.Ice.OptionalFormat.FSize))
        {
            int pos = ostr.startSize();
            CleaningScheduleListHelper.write(ostr, v);
            ostr.endSize(pos);
        }
    }

    public static java.util.Optional<CleaningSchedule[]> read(com.zeroc.Ice.InputStream istr, int tag)
    {
        if(istr.readOptional(tag, com.zeroc.Ice.OptionalFormat.FSize))
        {
            istr.skip(4);
            CleaningSchedule[] v;
            v = CleaningScheduleListHelper.read(istr);
            return java.util.Optional.of(v);
        }
        else
        {
            return java.util.Optional.empty();
        }
    }
}
