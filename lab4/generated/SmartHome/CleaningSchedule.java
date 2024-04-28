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

public class CleaningSchedule implements java.lang.Cloneable,
                                         java.io.Serializable
{
    public int id;

    public Room room;

    public Date date;

    public CleaningSchedule()
    {
        this.room = new Room();
        this.date = new Date();
    }

    public CleaningSchedule(int id, Room room, Date date)
    {
        this.id = id;
        this.room = room;
        this.date = date;
    }

    public boolean equals(java.lang.Object rhs)
    {
        if(this == rhs)
        {
            return true;
        }
        CleaningSchedule r = null;
        if(rhs instanceof CleaningSchedule)
        {
            r = (CleaningSchedule)rhs;
        }

        if(r != null)
        {
            if(this.id != r.id)
            {
                return false;
            }
            if(this.room != r.room)
            {
                if(this.room == null || r.room == null || !this.room.equals(r.room))
                {
                    return false;
                }
            }
            if(this.date != r.date)
            {
                if(this.date == null || r.date == null || !this.date.equals(r.date))
                {
                    return false;
                }
            }

            return true;
        }

        return false;
    }

    public int hashCode()
    {
        int h_ = 5381;
        h_ = com.zeroc.IceInternal.HashUtil.hashAdd(h_, "::SmartHome::CleaningSchedule");
        h_ = com.zeroc.IceInternal.HashUtil.hashAdd(h_, id);
        h_ = com.zeroc.IceInternal.HashUtil.hashAdd(h_, room);
        h_ = com.zeroc.IceInternal.HashUtil.hashAdd(h_, date);
        return h_;
    }

    public CleaningSchedule clone()
    {
        CleaningSchedule c = null;
        try
        {
            c = (CleaningSchedule)super.clone();
        }
        catch(CloneNotSupportedException ex)
        {
            assert false; // impossible
        }
        return c;
    }

    public void ice_writeMembers(com.zeroc.Ice.OutputStream ostr)
    {
        ostr.writeInt(this.id);
        Room.ice_write(ostr, this.room);
        Date.ice_write(ostr, this.date);
    }

    public void ice_readMembers(com.zeroc.Ice.InputStream istr)
    {
        this.id = istr.readInt();
        this.room = Room.ice_read(istr);
        this.date = Date.ice_read(istr);
    }

    static public void ice_write(com.zeroc.Ice.OutputStream ostr, CleaningSchedule v)
    {
        if(v == null)
        {
            _nullMarshalValue.ice_writeMembers(ostr);
        }
        else
        {
            v.ice_writeMembers(ostr);
        }
    }

    static public CleaningSchedule ice_read(com.zeroc.Ice.InputStream istr)
    {
        CleaningSchedule v = new CleaningSchedule();
        v.ice_readMembers(istr);
        return v;
    }

    static public void ice_write(com.zeroc.Ice.OutputStream ostr, int tag, java.util.Optional<CleaningSchedule> v)
    {
        if(v != null && v.isPresent())
        {
            ice_write(ostr, tag, v.get());
        }
    }

    static public void ice_write(com.zeroc.Ice.OutputStream ostr, int tag, CleaningSchedule v)
    {
        if(ostr.writeOptional(tag, com.zeroc.Ice.OptionalFormat.FSize))
        {
            int pos = ostr.startSize();
            ice_write(ostr, v);
            ostr.endSize(pos);
        }
    }

    static public java.util.Optional<CleaningSchedule> ice_read(com.zeroc.Ice.InputStream istr, int tag)
    {
        if(istr.readOptional(tag, com.zeroc.Ice.OptionalFormat.FSize))
        {
            istr.skip(4);
            return java.util.Optional.of(CleaningSchedule.ice_read(istr));
        }
        else
        {
            return java.util.Optional.empty();
        }
    }

    private static final CleaningSchedule _nullMarshalValue = new CleaningSchedule();

    /** @hidden */
    public static final long serialVersionUID = 2536944206314810460L;
}
