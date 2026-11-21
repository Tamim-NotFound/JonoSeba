import { apiGet, apiPost } from "./client";

export type ComplaintStatus =
  | "pending"
  | "in_progress"
  | "resolved"
  | "rejected";

export type ComplaintPriority =
  | "low"
  | "medium"
  | "high";

export interface Department {
  id: number;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Complaint {
  id: number;
  title: string;
  description: string;
  location: string;
  status: ComplaintStatus;
  priority: ComplaintPriority;
  citizen_id: number;
  department_id: number;
  created_at: string;
  updated_at: string;
}

export interface NewComplaintPayload {
  title: string;
  description: string;
  location: string;
  department_id: number;
}

export function getActiveDepartments(): Promise<Department[]> {
  return apiGet<Department[]>(
    "/departments?is_active=true",
  );
}

export function getMyComplaints(): Promise<Complaint[]> {
  return apiGet<Complaint[]>("/complaints");
}

export function getComplaintById(
  id: number,
): Promise<Complaint> {
  if (!Number.isSafeInteger(id) || id < 1) {
    throw new Error(
      "A valid positive complaint ID is required.",
    );
  }

  return apiGet<Complaint>(`/complaints/${id}`);
}

export function submitComplaint(
  data: NewComplaintPayload,
): Promise<Complaint> {
  return apiPost<Complaint>("/complaints", data);
}
