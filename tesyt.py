from pywinauto import Desktop

desktop = Desktop(backend="win32")

print("\n========================================")
print("       SAP PRINT BUTTON TEST")
print("========================================\n")

windows = desktop.windows(
    title="Print:",
    visible_only=True
)

if not windows:
    print("❌ Print window not found")
    exit()

print_window = windows[0]

print("✓ Print window found")
print("Handle:", print_window.handle)
print("Class :", print_window.class_name())
print()

buttons = print_window.descendants(class_name="Button")

print("Buttons found:", len(buttons))
print()

for i, button in enumerate(buttons):

    try:
        rect = button.rectangle()

        print(
            f"[{i}] "
            f"ClassNN=Button{i + 1} "
            f"Text={button.window_text()!r} "
            f"Handle={button.handle} "
            f"Position=({rect.left},{rect.top}) "
            f"Size=({rect.width()},{rect.height()})"
        )

    except Exception as e:
        print(f"[{i}] ERROR: {e}")


print()
print("----------------------------------------")
print("Expected Print button = Button3")
print("----------------------------------------")
print()

print("Press ENTER to CLICK Button3...")
input()

try:

    print_button = print_window.child_window(
        class_name="Button",
        found_index=2
    )

    print("Clicking Button3...")

    print_button.click()

    print("✓ Button3 clicked")

except Exception as e:

    print("❌ Could not click Button3")
    print("Error:", e)