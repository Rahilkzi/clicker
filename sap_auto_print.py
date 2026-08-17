import time
from pywinauto import Desktop


# ============================================================
# SAP AUTO PRINT AUTOMATION
# ============================================================

desktop = Desktop(backend="win32")

CHECK_INTERVAL = 0.2
ERROR_CHECK_INTERVAL = 0.2

# Maximum time to wait after clicking Print
PRINT_WAIT_TIMEOUT = 15

# Small delay after handling a print/error dialog
ACTION_DELAY = 0.5


# ============================================================
# STARTUP
# ============================================================

print()
print("=" * 70)
print("                    SAP AUTO PRINT")
print("=" * 70)
print()
print("Automation is running...")
print("Press Ctrl+C to stop.")
print()


# ============================================================
# FIND SAP PRINT WINDOWS
# ============================================================

def get_print_windows():

    result = []

    try:

        windows = desktop.windows(
            title="Print:",
            class_name="#32770",
            visible_only=True
        )

        for window in windows:

            try:

                if window.is_visible():
                    result.append(window)

            except Exception:
                pass

    except Exception:
        pass

    return result


# ============================================================
# FIND PDF ERROR WINDOWS
# ============================================================

def get_pdf_error_windows():

    result = []

    try:

        dialogs = desktop.windows(
            class_name="#32770",
            visible_only=True
        )

    except Exception:
        return result


    for dialog in dialogs:

        try:

            if not dialog.is_visible():
                continue


            title = dialog.window_text().strip()


            # ------------------------------------------------
            # PDF ERROR IDENTIFICATION
            #
            # Example:
            #
            # C:\temp\0999324283.pdf
            # ------------------------------------------------

            if not title.lower().endswith(".pdf"):
                continue


            # ------------------------------------------------
            # Find OK button
            # ------------------------------------------------

            ok_button = None

            try:

                buttons = dialog.descendants(
                    class_name="Button"
                )

                for button in buttons:

                    try:

                        text = (
                            button.window_text()
                            .strip()
                            .upper()
                        )

                        if text == "OK":

                            ok_button = button
                            break

                    except Exception:
                        pass

            except Exception:
                pass


            # ------------------------------------------------
            # Only accept dialog if OK button exists
            # ------------------------------------------------

            if ok_button is not None:

                result.append(
                    (dialog, ok_button)
                )

        except Exception:
            pass


    return result


# ============================================================
# FIND PRINT BUTTON
# ============================================================

def find_print_button(print_window):

    try:

        buttons = print_window.descendants(
            class_name="Button"
        )


        print(
            f"Buttons found: {len(buttons)}"
        )


        # ----------------------------------------------------
        # Your tested SAP Print dialog:
        #
        # [0] Button
        # [1] Button  ← PRINT
        # [2] Button
        # [3] Button
        #
        # The Print button has:
        #
        # Text     = ''
        # Position = approximately (443,619)
        # Size     = approximately (100,20)
        #
        # Therefore we use BUTTON INDEX 1.
        # ----------------------------------------------------

        if len(buttons) >= 2:

            candidate = buttons[2]

            try:

                if candidate.is_visible():

                    return candidate

            except Exception:
                pass


        return None


    except Exception as e:

        print(
            "Print button detection error:",
            repr(e)
        )

        return None


# ============================================================
# CLICK PRINT BUTTON
# ============================================================

def click_print(print_window):

    try:

        print()
        print("----------------------------------------")
        print("Finding PRINT button...")
        print("----------------------------------------")


        print_button = find_print_button(
            print_window
        )


        if print_button is None:

            print(
                "❌ PRINT button could not be identified."
            )

            return False


        # ----------------------------------------------------
        # Display information
        # ----------------------------------------------------

        try:

            print(
                "Handle   :",
                print_button.handle
            )

            print(
                "Class    :",
                print_button.class_name()
            )

            print(
                "Text     :",
                repr(print_button.window_text())
            )

            print(
                "Position :",
                print_button.rectangle()
            )

        except Exception:
            pass


        print()
        print("Clicking PRINT button...")


        # ----------------------------------------------------
        # Use Windows control click.
        #
        # This does NOT depend on mouse coordinates.
        # ----------------------------------------------------

        print_button.click()


        print("✓ PRINT button clicked successfully.")

        return True


    except Exception as e:

        print()
        print(
            "❌ Could not click PRINT button."
        )

        print(
            "Error:",
            repr(e)
        )

        return False


# ============================================================
# CLOSE PDF ERROR
# ============================================================

def close_pdf_error(dialog, ok_button):

    try:

        print()
        print("=" * 70)
        print("                  PDF ERROR DETECTED")
        print("=" * 70)


        print(
            "Dialog title:",
            repr(dialog.window_text())
        )


        print(
            "Dialog handle:",
            dialog.handle
        )


        print(
            "OK handle:",
            ok_button.handle
        )


        print()
        print("Clicking OK...")


        # ----------------------------------------------------
        # Click OK using Windows UI automation
        # ----------------------------------------------------

        ok_button.click()


        print("✓ PDF error closed.")


        return True


    except Exception as e:

        print()
        print(
            "❌ Could not close PDF error."
        )

        print(
            "Error:",
            repr(e)
        )

        return False


# ============================================================
# WAIT FOR PRINT RESULT
# ============================================================

def wait_after_print(print_window):

    start_time = time.time()


    print()
    print("----------------------------------------")
    print("Waiting for print result...")
    print("----------------------------------------")


    while (
        time.time() - start_time
        < PRINT_WAIT_TIMEOUT
    ):

        # ====================================================
        # 1. CHECK PDF ERROR FIRST
        # ====================================================

        errors = get_pdf_error_windows()


        if errors:

            print()
            print(
                "PDF error window detected."
            )


            for dialog, ok_button in errors:

                close_pdf_error(
                    dialog,
                    ok_button
                )


            # ------------------------------------------------
            # Error handled.
            #
            # IMPORTANT:
            # Do not immediately click Print again.
            # Wait for SAP to move to the next item.
            # ------------------------------------------------

            time.sleep(
                ACTION_DELAY
            )

            return "ERROR"


        # ====================================================
        # 2. CHECK WHETHER PRINT WINDOW CLOSED
        # ====================================================

        try:

            if not print_window.exists():

                print()
                print(
                    "✓ Print window closed."
                )

                return "SUCCESS"

        except Exception:

            # If the window handle is no longer valid,
            # treat it as closed.

            return "SUCCESS"


        # ====================================================
        # 3. CHECK AGAIN
        # ====================================================

        time.sleep(
            ERROR_CHECK_INTERVAL
        )


    # ========================================================
    # TIMEOUT
    # ========================================================

    print()
    print(
        "⚠ Print operation timed out."
    )

    return "TIMEOUT"


# ============================================================
# PROCESSED WINDOW TRACKING
# ============================================================

# ------------------------------------------------------------
# This prevents the automation from clicking the SAME
# Print dialog repeatedly if an error dialog appears while
# the Print window remains open.
# ------------------------------------------------------------

processed_print_handles = set()


# ============================================================
# MAIN AUTOMATION LOOP
# ============================================================

while True:

    try:

        # ====================================================
        # 1. PDF ERROR HAS HIGHEST PRIORITY
        # ====================================================

        errors = get_pdf_error_windows()


        if errors:

            for dialog, ok_button in errors:

                close_pdf_error(
                    dialog,
                    ok_button
                )


            time.sleep(
                ACTION_DELAY
            )

            continue


        # ====================================================
        # 2. FIND SAP PRINT WINDOWS
        # ====================================================

        print_windows = get_print_windows()


        if not print_windows:

            time.sleep(
                CHECK_INTERVAL
            )

            continue


        # ====================================================
        # 3. PROCESS AVAILABLE PRINT WINDOWS
        # ====================================================

        for print_window in print_windows:

            try:

                handle = print_window.handle


                # ------------------------------------------------
                # Ignore a Print dialog already processed.
                # ------------------------------------------------

                if handle in processed_print_handles:

                    continue


                # ------------------------------------------------
                # Mark it immediately.
                #
                # This prevents repeated clicking if a PDF
                # error appears and the Print window remains.
                # ------------------------------------------------

                processed_print_handles.add(
                    handle
                )


                print()
                print("=" * 70)
                print("                 PRINT WINDOW DETECTED")
                print("=" * 70)


                print(
                    "Handle:",
                    handle
                )


                try:

                    print(
                        "PID   :",
                        print_window.element_info.process_id
                    )

                except Exception:
                    pass


                print(
                    "Title :",
                    repr(
                        print_window.window_text()
                    )
                )


                # =================================================
                # 4. CLICK PRINT
                # =================================================

                clicked = click_print(
                    print_window
                )


                if not clicked:

                    print()
                    print(
                        "⚠ PRINT button was not clicked."
                    )


                    # Allow this window to be retried
                    processed_print_handles.discard(
                        handle
                    )

                    continue


                # =================================================
                # 5. WAIT FOR RESULT
                # =================================================

                result = wait_after_print(
                    print_window
                )


                # =================================================
                # RESULT
                # =================================================

                if result == "SUCCESS":

                    print()
                    print(
                        "✓ PRINT COMPLETED."
                    )


                elif result == "ERROR":

                    print()
                    print(
                        "✓ PDF ERROR HANDLED."
                    )


                elif result == "TIMEOUT":

                    print()
                    print(
                        "⚠ PRINT RESULT TIMEOUT."
                    )


                print()
                print(
                    "Waiting for next SAP print..."
                )


                time.sleep(
                    ACTION_DELAY
                )


            except Exception as e:

                print()
                print(
                    "Print window processing error:",
                    repr(e)
                )

                continue


        # ====================================================
        # 6. CLEAN OLD HANDLES
        # ====================================================

        # ----------------------------------------------------
        # Remove handles that no longer exist.
        #
        # This allows Windows to reuse handles safely.
        # ----------------------------------------------------

        current_handles = set()

        for window in print_windows:

            try:

                current_handles.add(
                    window.handle
                )

            except Exception:
                pass


        processed_print_handles.intersection_update(
            current_handles
        )


        time.sleep(
            CHECK_INTERVAL
        )


    # ========================================================
    # CTRL+C
    # ========================================================

    except KeyboardInterrupt:

        print()
        print()
        print("=" * 70)
        print("                 SAP AUTO PRINT STOPPED")
        print("=" * 70)
        print()

        break


    # ========================================================
    # UNEXPECTED ERROR
    # ========================================================

    except Exception as e:

        print()
        print(
            "Main automation error:",
            repr(e)
        )

        print(
            "Automation will continue..."
        )

        time.sleep(1)