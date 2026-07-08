import { apiRequest } from './Api'

export const getAllBookings = async () => {
    let response;
    try {
        response = await apiRequest("/api/rooms", {
            method: "GET",
        });
    } catch (e) {
        throw e;
    }
    return response
}

export const getBookingById = async ({room_name, id}) => {
    let response;
    
    try {
        response = await apiRequest(`/api/rooms/${room_name}/bookings/${id}`, {
            method: "GET",
        })
    } catch (e) {
        throw e;
    }
    return response
}

export const getBookings = async (room_name) => {
    let response;
    try {
        response = await apiRequest(`/api/rooms/${room_name}/bookings`, {
            method: "GET",
        });
    } catch (e) {
        throw e;
    }
    return response
}

export const postBookings = async ({
    room_name,
    intra,
    begin_at,
    end_at,
    isStaff
    }) => {
    let response;
    
    try {
        response = await apiRequest(`/api/rooms/${room_name}/bookings`, {
            method: "POST",
            body:   JSON.stringify({ intra, begin_at, end_at, isStaff })
        });
    } catch (e) {
        throw e;
    }
    return response
}

export const patchBookingById = async ({
    room_name,
    id,
    intra,
    begin_at,
    end_at
    }) => {
    let response;

    try {
        response = await apiRequest(`/api/rooms/${room_name}/bookings/${id}`, {
            method: "PATCH",
            body: JSON.stringify({intra, begin_at, end_at}),
        });
    } catch (e) {
        throw e;
    }
    return response
}

export const deleteBookingById = async ({room_name, id}) => {
    let response;
    
    try {
        response = await apiRequest(`/api/rooms/${room_name}/bookings/${id}`, {
            method: "DELETE",
        });
    } catch (e) {
        throw e;
    }
    return response
}
