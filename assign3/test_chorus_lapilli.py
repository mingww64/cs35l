#!/usr/bin/env python3
import unittest
import os
import sys
import argparse
import subprocess
import unittest
import urllib.request


class TestChorusLapilli(unittest.TestCase):
    '''Integration testing for Chorus Lapilli

    This class handles the entire react start up, testing, and take down
    process. Feel free to modify it to suit your needs.
    '''

    # ========================== [USEFUL CONSTANTS] ===========================

    # Vite default startup address
    VITE_HOST_ADDR = 'http://localhost:5173'

    # XPATH query used to find Chorus Lapilli board tiles
    BOARD_TILE_XPATH = '//button[contains(@class, \'square\')]'

    # Sets of symbol classes - each string contains all valid characters
    # for that particular symbol
    SYMBOL_BLANK = ''
    SYMBOL_X = 'Xx'
    SYMBOL_O = '0Oo'

    # ======================== [SETUP/TEARDOWN HOOKS] =========================

    @classmethod
    def setUpClass(cls):
        '''This function runs before testing occurs.

        Bring up the web app and configure Selenium
        '''

        env = dict(os.environ)
        env.update({
            # Prevent React from starting its own browser window
            'BROWSER': 'none',
        })

        subprocess.run(['npm', 'install'],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           env=env,
                           check=True)

        # Await Webserver Start
        cls.vite = subprocess.Popen(
            ['npm', 'run', 'dev'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=env)

        if cls.vite.stdout is None:
            raise OSError("Vite failed to start")
        for _ in cls.vite.stdout:
            try:
                with urllib.request.urlopen(cls.VITE_HOST_ADDR):
                    break

            except IOError:
                pass

            # Ensure Vite does not terminate early
            if cls.vite.poll() is not None:
                raise OSError('Vite terminated before test')
        if cls.vite.poll() is not None:
            raise OSError('Vite terminated before test')

        cls.driver = Browser()
        cls.driver.get(cls.VITE_HOST_ADDR)
        cls.driver.implicitly_wait(0.5)

    @classmethod
    def tearDownClass(cls):
        '''This function runs after all testing have run.

        Terminate Vite and take down the Selenium webdriver.
        '''
        cls.vite.terminate()
        cls.vite.wait()
        cls.driver.quit()

    def setUp(self):
        '''This function runs before every test.

        Refresh the browser so we get a new board.
        '''
        self.driver.refresh()

    def tearDown(self):
        '''This function runs after every test.

        Not needed, but feel free to add stuff here.
        '''

    # ========================== [HELPER FUNCTIONS] ===========================

    def assertBoardEmpty(self, tiles):
        '''Checks if all board tiles are empty.

        Arguments:
          tiles: List[WebElement] - a board consisting of 9 buttons elements
        '''
        if len(tiles) != 9:
            raise AssertionError('tiles is not a 3x3 grid')
        for i, tile in enumerate(tiles):
            if tile.text.strip():
                raise AssertionError(f'tile {i} is not empty: '
                                     f'\'{tile.text}\'')

    def assertTileIs(self, tile, symbol_set):
        '''Checks if a certain tile has a certain symbol.

        Arguments:
          tile: WebElement - the button element to check
          symbol_set: str - a string containing all the valid symbols
        Raises:
          AssertionError - if tile is not in the symbol set
        '''
        if symbol_set is None:
            return
        if symbol_set == self.SYMBOL_BLANK:
            name = 'BLANK'
        elif symbol_set == self.SYMBOL_X:
            name = 'X'
        elif symbol_set == self.SYMBOL_O:
            name = 'O'
        else:
            name = 'in symbol_set'
        text = tile.text.strip()
        if ((symbol_set == self.SYMBOL_BLANK and text)
                or (symbol_set != self.SYMBOL_BLANK and not text)
                or text not in symbol_set):
            raise AssertionError(f'tile is not {name}: \'{tile.text}\'')


# =========================== [ADD YOUR TESTS HERE] ===========================

    def test_new_board_empty(self):
        '''Check if a new game always starts with an empty board.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        self.assertBoardEmpty(tiles)

    def test_button_click(self):
        '''Check if clicking the top-left button adds an X.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        self.assertTileIs(tiles[0], self.SYMBOL_BLANK)
        tiles[0].click()
        self.assertTileIs(tiles[0], self.SYMBOL_X)

    def test_repeated_tile_swaps(self):
        '''Test repeated swapping of pieces between adjacent tiles'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        
        # Place initial X pieces
        tiles[0].click()  # X in top-left
        tiles[4].click()  # O in center
        tiles[1].click()  # X in top-middle
        tiles[3].click()  # O in middle-left
        tiles[2].click()  # X in top-right
        tiles[5].click()  # O in middle-right

        # Now X has three pieces (positions 0,1,2) and can start moving
        # Swap X piece between positions 1 and 4 multiple times
        tiles[1].click()  # Select X in top-middle
        tiles[4].click()  # Move to center
        self.assertTileIs(tiles[4], self.SYMBOL_X)
        self.assertTileIs(tiles[1], self.SYMBOL_BLANK)

        tiles[4].click()  # Select X in center
        tiles[1].click()  # Move back to top-middle
        self.assertTileIs(tiles[1], self.SYMBOL_X)
        self.assertTileIs(tiles[4], self.SYMBOL_BLANK)

        # Do it one more time
        tiles[1].click()  # Select X in top-middle
        tiles[4].click()  # Move to center
        self.assertTileIs(tiles[4], self.SYMBOL_X)
        self.assertTileIs(tiles[1], self.SYMBOL_BLANK)

    def test_center_move_rule(self):
        '''Test that a player must move out of center if no winning move'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        
        # Place pieces to set up the test
        tiles[4].click()  # X in center
        tiles[0].click()  # O in top-left
        tiles[1].click()  # X in top-middle
        tiles[3].click()  # O in middle-left
        tiles[7].click()  # X in bottom-middle
        tiles[6].click()  # O in bottom-left

        # X has pieces in center(4), top-middle(1), and bottom-middle(7)
        # Try to move piece from top-middle to top-right (should fail as center piece must move)
        tiles[1].click()  # Try to select X in top-middle
        self.assertTileIs(tiles[1], self.SYMBOL_X)  # Piece should still be there

        # Now move from center (which is required)
        tiles[4].click()  # Select center piece
        tiles[2].click()  # Move to top-right
        self.assertTileIs(tiles[4], self.SYMBOL_BLANK)
        self.assertTileIs(tiles[2], self.SYMBOL_X)

    def test_adjacent_moves_only(self):
        '''Test that pieces can only move to adjacent squares'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        
        # Place initial pieces
        tiles[0].click()  # X in top-left
        tiles[4].click()  # O in center
        tiles[1].click()  # X in top-middle
        tiles[3].click()  # O in middle-left
        tiles[2].click()  # X in top-right
        tiles[5].click()  # O in middle-right

        # Try to move X from top-left to bottom-right (non-adjacent)
        tiles[0].click()  # Select X in top-left
        tiles[8].click()  # Try to move to bottom-right (should fail)
        self.assertTileIs(tiles[0], self.SYMBOL_X)  # X should still be in top-left
        self.assertTileIs(tiles[8], self.SYMBOL_BLANK)  # Bottom-right should still be empty

        # Now try a valid adjacent move
        tiles[0].click()  # Select X in top-left
        tiles[3].click()  # Move to middle-left (adjacent)
        self.assertTileIs(tiles[0], self.SYMBOL_BLANK)
        self.assertTileIs(tiles[3], self.SYMBOL_X)


# ================= [DO NOT MAKE ANY CHANGES BELOW THIS LINE] =================

if __name__ != '__main__':
    from selenium.webdriver import Firefox as Browser
    from selenium.webdriver.common.by import By
else:
    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='Chorus Lapilli Tester')
    parser.add_argument('-b',
                        '--browser',
                        action='store',
                        metavar='name',
                        choices=['firefox', 'chrome', 'safari'],
                        default='firefox',
                        help='the browser to run tests with')
    parser.add_argument('-c',
                        '--change-dir',
                        action='store',
                        metavar='dir',
                        default=None,
                        help=('change the working directory before running '
                              'tests'))

    # Change the working directory
    options = parser.parse_args(sys.argv[1:])
    # Import different browser drivers based on user selection
    try:
        if options.browser == 'firefox':
            from selenium.webdriver import Firefox as Browser
        elif options.browser == 'chrome':
            from selenium.webdriver import Chrome as Browser
        else:
            from selenium.webdriver import Safari as Browser
        from selenium.webdriver.common.by import By
    except ImportError as err:
        print('[Error]',
              err, '\n\n'
              'Please refer to the Selenium documentation on installing the '
              'webdriver:\n'
              'https://www.selenium.dev/documentation/webdriver/'
              'getting_started/',
              file=sys.stderr)
        sys.exit(1)

    if options.change_dir:
        try:
            os.chdir(options.change_dir)
        except OSError as err:
            print(err, file=sys.stderr)
            sys.exit(1)

    if not os.path.isfile('package.json'):
        print('Invalid directory: cannot find \'package.json\'',
              file=sys.stderr)
        sys.exit(1)

    tests = unittest.defaultTestLoader.loadTestsFromTestCase(TestChorusLapilli)
    unittest.TextTestRunner().run(tests)
