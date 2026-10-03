import { render, screen } from "@testing-library/react";
import { vi, test, expect } from "vitest";
import App from "./App";

test("shows todos from the API", async () => {
  global.fetch = vi.fn(() =>
    Promise.resolve({ json: () => Promise.resolve([{ id: 1, title: "milk", done: false }]) })
  );
  render(<App />);
  expect(await screen.findByText("milk")).toBeTruthy();
});