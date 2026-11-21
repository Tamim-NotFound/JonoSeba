import { ApiError } from "./auth";

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "/api/v1"
).replace(/\/+$/, "");

const TOKEN_KEY = "jonoseba-access-token";

function getAccessToken(): string {
  let token: string | null = null;

  try {
    token = sessionStorage.getItem(TOKEN_KEY);
  } catch {
    throw new ApiError(
      "Browser session storage is unavailable.",
      0,
    );
  }

  if (!token) {
    throw new ApiError(
      "Please sign in to continue.",
      401,
    );
  }

  return token;
}

function getErrorMessage(
  body: unknown,
  fallback: string,
): string {
  if (!body || typeof body !== "object") {
    return fallback;
  }

  const data = body as Record<string, unknown>;

  if (typeof data.detail === "string") {
    return data.detail;
  }

  if (Array.isArray(data.detail)) {
    const messages = data.detail
      .map((item: unknown) => {
        if (
          item &&
          typeof item === "object" &&
          "msg" in item &&
          typeof item.msg === "string"
        ) {
          return item.msg;
        }

        return null;
      })
      .filter(
        (value): value is string => value !== null,
      );

    if (messages.length > 0) {
      return messages.join("; ");
    }
  }

  if (typeof data.message === "string") {
    return data.message;
  }

  return fallback;
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  if (!path.startsWith("/") || path.startsWith("//")) {
    throw new Error(
      "API path must start with a single slash.",
    );
  }

  const token = getAccessToken();

  const headers = new Headers(options.headers);

  headers.set("Authorization", `Bearer ${token}`);
  headers.set("Accept", "application/json");

  if (
    typeof options.body === "string" &&
    !headers.has("Content-Type")
  ) {
    headers.set("Content-Type", "application/json");
  }

  let response: Response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers,
      credentials: "omit",
    });
  } catch {
    throw new ApiError(
      "Could not connect to FastAPI. Check the backend server.",
      0,
    );
  }

  if (response.status === 204) {
    return undefined as T;
  }

  let body: unknown = null;

  try {
    body = await response.json();
  } catch {
    // Some error responses do not contain JSON.
  }

  if (!response.ok) {
    throw new ApiError(
      getErrorMessage(
        body,
        `API request failed (HTTP ${response.status}).`,
      ),
      response.status,
    );
  }

  return body as T;
}

export function apiGet<T>(path: string): Promise<T> {
  return apiRequest<T>(path, {
    method: "GET",
  });
}

export function apiPost<T>(
  path: string,
  data: unknown,
): Promise<T> {
  return apiRequest<T>(path, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function apiPatch<T>(
  path: string,
  data: unknown,
): Promise<T> {
  return apiRequest<T>(path, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}
