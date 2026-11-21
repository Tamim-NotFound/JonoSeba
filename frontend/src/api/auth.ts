
export interface UserProfile {
  id: number;
  full_name: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface RegisterPayload {
  full_name: string;
  email: string;
  password: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "/api/v1"
).replace(/\/+$/, "");

export class ApiError extends Error {
  public readonly status: number;

  constructor(
    message: string,
    status: number,
  ) {
    super(message);

    this.name = "ApiError";
    this.status = status;
  }
}

function extractMessage(
  body: unknown,
  fallback: string,
): string {
  if (typeof body !== "object" || body === null) {
    return fallback;
  }

  const detail = (body as { detail?: unknown }).detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    const messages = detail
      .map((entry: unknown) => {
        if (
          typeof entry === "object" &&
          entry !== null &&
          "msg" in entry &&
          typeof entry.msg === "string"
        ) {
          return entry.msg;
        }

        return null;
      })
      .filter(
        (message): message is string => message !== null,
      );

    if (messages.length > 0) {
      return messages.join(". ");
    }
  }

  if (
    "message" in body &&
    typeof body.message === "string"
  ) {
    return body.message;
  }

  return fallback;
}

async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: {
        Accept: "application/json",
        ...(options.body
          ? { "Content-Type": "application/json" }
          : {}),
        ...options.headers,
      },
      credentials: "omit",
    });
  } catch {
    throw new ApiError(
      "Cannot connect to the server. Check that FastAPI is running.",
      0,
    );
  }

  let body: unknown = null;

  try {
    body = await response.json();
  } catch {
    // Some responses may not contain JSON.
  }

  if (!response.ok) {
    throw new ApiError(
      extractMessage(
        body,
        `Request failed (HTTP ${response.status}).`,
      ),
      response.status,
    );
  }

  return body as T;
}

export function registerCitizen(
  payload: RegisterPayload,
): Promise<UserProfile> {
  return request<UserProfile>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function loginCitizen(
  payload: LoginPayload,
): Promise<TokenResponse> {
  return request<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getMyProfile(
  token: string,
): Promise<UserProfile> {
  return request<UserProfile>("/auth/me", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
