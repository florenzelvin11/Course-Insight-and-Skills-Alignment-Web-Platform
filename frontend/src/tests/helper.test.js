import { apiCall, runFetch, getOptions, setUserData, clearUserData, getUserData, logOut, canAdd } from "../helpers/helper";

const port = require('../config.json').BACKEND_PORT;
export const apiUrl = `http://localhost:${port}`;

describe('apiCall', () => {
  it('should handle successful API call', async () => {
    const mockResponse = { message: 'Success' };
    const mockJsonPromise = Promise.resolve(mockResponse);
    const mockFetchPromise = Promise.resolve({
      json: () => mockJsonPromise,
      ok: true,
    });

    global.fetch = jest.fn().mockImplementation(() => mockFetchPromise);

    const response = await apiCall('GET', '/example', {});
    expect(response).toEqual(mockResponse);
    expect(global.fetch).toHaveBeenCalledWith(`${apiUrl}/example`, {
      method: 'GET',
      body: JSON.stringify({}),
      headers: {
        'Content-Type': 'application/json',
      },
    });
  });

  it('should handle API call error', async () => {
    const errorMessage = 'error message';
    const mockJsonPromise = Promise.reject(new Error(errorMessage));
    const mockFetchPromise = Promise.resolve({
      json: () => mockJsonPromise,
      ok: false,
    });

    global.fetch = jest.fn().mockImplementation(() => mockFetchPromise);

    const response = await apiCall('GET', '/example', {});
    expect(response).toEqual({ error: `Error making GET request to /example: ${errorMessage}` });
    expect(global.fetch).toHaveBeenCalledWith(`${apiUrl}/example`, {
      method: 'GET',
      body: JSON.stringify({}),
      headers: {
        'Content-Type': 'application/json',
      },
    });
  });
});

describe('runFetch', () => {
  it('should handle successful fetch', async () => {
    const mockResponse = { message: 'Success' };
    const mockJsonPromise = Promise.resolve(mockResponse);

    global.fetch = jest.fn().mockImplementation(() =>
      Promise.resolve({
        json: () => mockJsonPromise,
        ok: true,
      })
    );

    const response = await runFetch('GET', '/example', {});

    expect(response).toEqual(mockResponse);
  });

  it('should handle fetch error', async () => {
    const errorMessage = 'Error message';
    const mockJsonPromise = Promise.reject(new Error(errorMessage));

    global.fetch = jest.fn().mockImplementation(() =>
      Promise.resolve({
        json: () => mockJsonPromise,
        ok: false,
      })
    );

    try {
      await runFetch('GET', '/example', {});
    } catch (error) {
      expect(error.message).toEqual(`Error making GET request to /example: ${errorMessage}`);
    }
  });
});

describe('getOptions', () => {
  it('should return correct options', async () => {
    clearUserData();
    const returnValue = getOptions('GET',{test: 'test'});

    expect(returnValue).toEqual( {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({test: 'test'}),
    });
  });

  it('should return correct options with correct user data', async () => {
    setUserData({token: 'testToken'})
    const returnValue = getOptions('GET',{test: 'test'});

    expect(returnValue).toEqual( {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer testToken`
      },
      body: JSON.stringify({test: 'test'}),
    });
  });

  it('should return correct options with no body', async () => {
    clearUserData();
    const returnValue = getOptions('GET');

    expect(returnValue).toEqual( {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  });
});

describe('setUserData, getUserData', () => {
  it('should set user data', async () => {
    clearUserData();
    setUserData({test: 'test'})
    expect(getUserData()).toEqual({
      test: 'test'
    })
  });

  it('should add to exisitng user data', async () => {
    clearUserData();
    setUserData({test: 'test'})
    expect(getUserData()).toEqual({
      test: 'test'
    })

    setUserData({testOne: 'testOne'})

    expect(getUserData()).toEqual({
      test: 'test',
      testOne: 'testOne'
    })
  });

  it('should override to exisitng user data if the same key is used', async () => {
    clearUserData();
    setUserData({test: 'old'})
    expect(getUserData()).toEqual({
      test: 'old'
    })

    setUserData({test: 'new'})

    expect(getUserData()).toEqual({
      test: 'new',
    })
  });
});

describe('clearUserData', () => {
  it('should clear user data', async () => {
    clearUserData();
    setUserData({test: 'test'})
    expect(getUserData()).toEqual({
      test: 'test'
    })
    clearUserData();
    expect(getUserData()).toBeNull();
  });
});

describe('logOut', () => {
  it('should clear user data', async () => {
    clearUserData();
    setUserData({test: 'test'})
    expect(getUserData()).toEqual({
      test: 'test'
    })
    logOut();
    expect(getUserData()).toBeNull();
  });

  it('should call logout endpoint', async () => {
    clearUserData();
    const mockResponse = { message: 'Success' };
    const mockJsonPromise = Promise.resolve(mockResponse);
    const mockFetchPromise = Promise.resolve({
      json: () => mockJsonPromise,
      ok: true,
    });
    global.fetch = jest.fn().mockImplementation(() => mockFetchPromise);

    logOut();

    expect(global.fetch).toHaveBeenCalledWith(`${apiUrl}/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  });
});

describe('canAdd', () => {
  it('should return false is no user data', async () => {
    clearUserData();

    expect(canAdd()).toBe(false);
  });

  it('should return ture is userType is academic', async () => {
    clearUserData();
    setUserData({userType: 'academic'})

    expect(canAdd()).toBe(true);
  });

  it('should return ture is userType is admin', async () => {
    clearUserData();
    setUserData({userType: 'admin'})

    expect(canAdd()).toBe(true);
  });
});
