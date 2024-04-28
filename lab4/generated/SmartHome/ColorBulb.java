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

public interface ColorBulb extends DimmableBulb
{
    void setColor(Color color, com.zeroc.Ice.Current current)
        throws InvalidColorError;

    Color getColor(com.zeroc.Ice.Current current);

    /** @hidden */
    static final String[] _iceIds =
    {
        "::Ice::Object",
        "::SmartHome::ColorBulb",
        "::SmartHome::Device",
        "::SmartHome::DimmableBulb",
        "::SmartHome::SimpleBulb"
    };

    @Override
    default String[] ice_ids(com.zeroc.Ice.Current current)
    {
        return _iceIds;
    }

    @Override
    default String ice_id(com.zeroc.Ice.Current current)
    {
        return ice_staticId();
    }

    static String ice_staticId()
    {
        return "::SmartHome::ColorBulb";
    }

    /**
     * @hidden
     * @param obj -
     * @param inS -
     * @param current -
     * @return -
     * @throws com.zeroc.Ice.UserException -
    **/
    static java.util.concurrent.CompletionStage<com.zeroc.Ice.OutputStream> _iceD_setColor(ColorBulb obj, final com.zeroc.IceInternal.Incoming inS, com.zeroc.Ice.Current current)
        throws com.zeroc.Ice.UserException
    {
        com.zeroc.Ice.Object._iceCheckMode(com.zeroc.Ice.OperationMode.Idempotent, current.mode);
        com.zeroc.Ice.InputStream istr = inS.startReadParams();
        Color iceP_color;
        iceP_color = Color.ice_read(istr);
        inS.endReadParams();
        obj.setColor(iceP_color, current);
        return inS.setResult(inS.writeEmptyParams());
    }

    /**
     * @hidden
     * @param obj -
     * @param inS -
     * @param current -
     * @return -
    **/
    static java.util.concurrent.CompletionStage<com.zeroc.Ice.OutputStream> _iceD_getColor(ColorBulb obj, final com.zeroc.IceInternal.Incoming inS, com.zeroc.Ice.Current current)
    {
        com.zeroc.Ice.Object._iceCheckMode(com.zeroc.Ice.OperationMode.Idempotent, current.mode);
        inS.readEmptyParams();
        Color ret = obj.getColor(current);
        com.zeroc.Ice.OutputStream ostr = inS.startWriteParams();
        Color.ice_write(ostr, ret);
        inS.endWriteParams(ostr);
        return inS.setResult(ostr);
    }

    /** @hidden */
    final static String[] _iceOps =
    {
        "getBrightness",
        "getColor",
        "getDeviceName",
        "ice_id",
        "ice_ids",
        "ice_isA",
        "ice_ping",
        "isTurnedOn",
        "setBrightness",
        "setColor",
        "turnOff",
        "turnOn"
    };

    /** @hidden */
    @Override
    default java.util.concurrent.CompletionStage<com.zeroc.Ice.OutputStream> _iceDispatch(com.zeroc.IceInternal.Incoming in, com.zeroc.Ice.Current current)
        throws com.zeroc.Ice.UserException
    {
        int pos = java.util.Arrays.binarySearch(_iceOps, current.operation);
        if(pos < 0)
        {
            throw new com.zeroc.Ice.OperationNotExistException(current.id, current.facet, current.operation);
        }

        switch(pos)
        {
            case 0:
            {
                return DimmableBulb._iceD_getBrightness(this, in, current);
            }
            case 1:
            {
                return _iceD_getColor(this, in, current);
            }
            case 2:
            {
                return Device._iceD_getDeviceName(this, in, current);
            }
            case 3:
            {
                return com.zeroc.Ice.Object._iceD_ice_id(this, in, current);
            }
            case 4:
            {
                return com.zeroc.Ice.Object._iceD_ice_ids(this, in, current);
            }
            case 5:
            {
                return com.zeroc.Ice.Object._iceD_ice_isA(this, in, current);
            }
            case 6:
            {
                return com.zeroc.Ice.Object._iceD_ice_ping(this, in, current);
            }
            case 7:
            {
                return Device._iceD_isTurnedOn(this, in, current);
            }
            case 8:
            {
                return DimmableBulb._iceD_setBrightness(this, in, current);
            }
            case 9:
            {
                return _iceD_setColor(this, in, current);
            }
            case 10:
            {
                return Device._iceD_turnOff(this, in, current);
            }
            case 11:
            {
                return Device._iceD_turnOn(this, in, current);
            }
        }

        assert(false);
        throw new com.zeroc.Ice.OperationNotExistException(current.id, current.facet, current.operation);
    }
}