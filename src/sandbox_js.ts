import { task } from "@capsule-run/sdk";

export const executeCode = task(
  { name: "executeCode", compute: "HIGH"},
  async (code: string): Promise<any> => {
    const fn = new Function(code);
    return fn();
  }
);

export const main = task(
  { name: "main", compute: "HIGH"},
  async (code: string): Promise<any> => {
    const response = await executeCode(code);
    return response.result;
  }
);
