const API_URL = import.meta.env.VITE_API_URL

/**
 * Helper function for making API requests. Abstraction to help other API calls easier.
 * 
 * @param endpoint API endpoint path (starting with /)
 * @param options fetch options
 * @returns Promise with the API response
 * @throws Error with message from API or generic error
 */
export const apiRequest = async (endpoint, options = {}) => {
    let response;
    
    try {
        response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers: {
                'Content-type': 'application/json',
                ...(options.headers || {})
            },
            credentials: "include",
        });
    } catch (e) {
        throw new Error('Network error. Please check your connection and try again')
    }

    const contentType = response.headers.get('content-type');

    const data = contentType && contentType.includes('application/json')
        ? await response.json()
        : await response.text();

    if (!response.ok) {
        const message = (typeof data === 'object' && data !== null && 'detail' in data)
            ? data.detail
            : `Request failed with status ${response.status}`;
        throw new Error(message);
    }
    
    return data;
}
