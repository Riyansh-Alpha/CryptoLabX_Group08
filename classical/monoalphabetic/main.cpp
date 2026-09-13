#include <iostream>
#include <fstream>
#include <string>

using namespace std;

char toUpperManual(char c)
{
    if (c >= 'a' && c <= 'z')
        return c - 'a' + 'A';

    return c;
}

string apply_substitution(const string& text, const string& key)
{
    string result = "";

    for (int i = 0; i < (int)text.length(); i++)
    {
        char c = text[i];

        c = toUpperManual(c);

        if (c >= 'A' && c <= 'Z')
        {
            int index = c - 'A';
            result += key[index];
        }
        else
        {
            result += c;
        }
    }

    return result;
}

// FREQUENCY ANALYSIS
void frequency_analysis(const string& ciphertext)
{
    int frequency[26] = {0};
    int totalLetters = 0;

    for (int i = 0; i < (int)ciphertext.length(); i++)
    {
        char c = toUpperManual(ciphertext[i]);

        if (c >= 'A' && c <= 'Z')
        {
            frequency[c - 'A']++;
            totalLetters++;
        }
    }

    cout << "        LETTER FREQUENCY ANALYSIS\n";

    bool used[26] = {false};

    cout << "\nLetter\tFrequency\tPercentage\n";

    for (int position = 0; position < 26; position++)
    {
        int maxFrequency = -1;
        int maxIndex = -1;

        for (int i = 0; i < 26; i++)
        {
            if (!used[i] && frequency[i] > maxFrequency)
            {
                maxFrequency = frequency[i];
                maxIndex = i;
            }
        }

        if (maxIndex == -1)
            break;

        used[maxIndex] = true;

        double percentage = 0;

        if (totalLetters > 0)
        {
            percentage =
                ((double)frequency[maxIndex] / totalLetters) * 100;
        }

        cout << char('A' + maxIndex)
             << "\t"
             << frequency[maxIndex]
             << "\t\t"
             << percentage
             << "%\n";
    }

    cout << "\nMost frequent ciphertext letters:\n";

    for (int i = 0; i < 5; i++)
    {
        int maxFrequency = -1;
        int maxIndex = -1;

        for (int j = 0; j < 26; j++)
        {
            if (frequency[j] > maxFrequency)
            {
                maxFrequency = frequency[j];
                maxIndex = j;
            }
        }

        if (maxIndex >= 0)
        {
            cout << char('A' + maxIndex)
                 << " -> "
                 << frequency[maxIndex]
                 << " occurrences\n";

            frequency[maxIndex] = -1;
        }
    }
}

// EXTRACT AND DISPLAY WORD FREQUENCY
void word_frequency_analysis(const string& ciphertext)
{
    string words[10000];
    int counts[10000];
    int wordCount = 0;

    string currentWord = "";

    for (int i = 0; i <= (int)ciphertext.length(); i++)
    {
        char c;

        if (i < (int)ciphertext.length())
            c = toUpperManual(ciphertext[i]);
        else
            c = ' ';

        if (c >= 'A' && c <= 'Z')
        {
            currentWord += c;
        }
        else
        {
            if (currentWord.length() > 0)
            {
                int found = -1;

                for (int j = 0; j < wordCount; j++)
                {
                    if (words[j] == currentWord)
                    {
                        found = j;
                        break;
                    }
                }

                if (found == -1)
                {
                    words[wordCount] = currentWord;
                    counts[wordCount] = 1;
                    wordCount++;
                }
                else
                {
                    counts[found]++;
                }

                currentWord = "";
            }
        }
    }

    cout << "\n============================================\n";
    cout << "          WORD FREQUENCY ANALYSIS\n";
    cout << "============================================\n";

    for (int i = 0; i < wordCount - 1; i++)
    {
        for (int j = i + 1; j < wordCount; j++)
        {
            if (counts[j] > counts[i])
            {
                int tempCount = counts[i];
                counts[i] = counts[j];
                counts[j] = tempCount;

                string tempWord = words[i];
                words[i] = words[j];
                words[j] = tempWord;
            }
        }
    }

    cout << "\nRepeated / frequent words:\n";

    for (int i = 0; i < wordCount; i++)
    {
        if (counts[i] > 1)
        {
            cout << words[i]
                 << " -> "
                 << counts[i]
                 << " times\n";
        }
    }

    cout << "\nOne-letter words:\n";

    for (int i = 0; i < wordCount; i++)
    {
        if (words[i].length() == 1)
        {
            cout << words[i]
                 << " -> "
                 << counts[i]
                 << " times\n";
        }
    }

    cout << "\nTwo-letter words:\n";

    for (int i = 0; i < wordCount; i++)
    {
        if (words[i].length() == 2)
        {
            cout << words[i]
                 << " -> "
                 << counts[i]
                 << " times\n";
        }
    }

    cout << "\nThree-letter words:\n";

    for (int i = 0; i < wordCount; i++)
    {
        if (words[i].length() == 3)
        {
            cout << words[i]
                 << " -> "
                 << counts[i]
                 << " times\n";
        }
    }
}

// GENERATE WORD PATTERN
//
// Example:
// THAT -> 0120
// LETTER -> 012213
string generate_pattern(const string& word)
{
    string pattern = "";
    char symbols[26];
    int assigned = 0;

    for (int i = 0; i < 26; i++)
        symbols[i] = '?';

    for (int i = 0; i < (int)word.length(); i++)
    {
        char c = word[i];

        int index = c - 'A';

        if (symbols[index] == '?')
        {
            symbols[index] = char('0' + assigned);
            assigned++;
        }

        pattern += symbols[index];
    }

    return pattern;
}

// PATTERN ANALYSIS
void pattern_analysis(const string& ciphertext)
{
    string word = "";

    cout << "\n============================================\n";
    cout << "             PATTERN ANALYSIS\n";
    cout << "============================================\n";

    for (int i = 0; i <= (int)ciphertext.length(); i++)
    {
        char c;

        if (i < (int)ciphertext.length())
            c = toUpperManual(ciphertext[i]);
        else
            c = ' ';

        if (c >= 'A' && c <= 'Z')
        {
            word += c;
        }
        else
        {
            if (word.length() > 0)
            {
                cout << word
                     << " -> "
                     << generate_pattern(word)
                     << "\n";

                word = "";
            }
        }
    }
}

// DISPLAY PARTIAL PLAINTEXT
//
// decryptKey[ciphertext letter] = plaintext letter
// '?' means substitution is not known yet.
void display_partial_plaintext(
    const string& ciphertext,
    const char decryptKey[26])
{
    cout << "\n============================================\n";
    cout << "           PARTIAL PLAINTEXT\n";
    cout << "============================================\n";

    for (int i = 0; i < (int)ciphertext.length(); i++)
    {
        char c = ciphertext[i];

        if (c >= 'A' && c <= 'Z')
        {
            int index = c - 'A';

            if (decryptKey[index] == '?')
                cout << '_';
            else
                cout << decryptKey[index];
        }
        else
        {
            cout << c;
        }
    }

    cout << "\n";
}

// ITERATIVE CRYPTANALYSIS
void interactive_cryptanalysis(
    const string& ciphertext,
    char decryptKey[26])
{
    while (true)
    {
        display_partial_plaintext(ciphertext, decryptKey);

        char cipherLetter;
        char plainLetter;

        cout << "\nEnter ciphertext letter (0 to finish): ";
        cin >> cipherLetter;

        if (cipherLetter == '0')
            break;

        cipherLetter = toUpperManual(cipherLetter);

        if (cipherLetter < 'A' || cipherLetter > 'Z')
        {
            cout << "Invalid ciphertext letter.\n";
            continue;
        }

        cout << "Enter suspected plaintext letter: ";
        cin >> plainLetter;

        plainLetter = toUpperManual(plainLetter);

        if (plainLetter < 'A' || plainLetter > 'Z')
        {
            cout << "Invalid plaintext letter.\n";
            continue;
        }

        int cipherIndex = cipherLetter - 'A';

        bool alreadyUsed = false;

        for (int i = 0; i < 26; i++)
        {
            if (i != cipherIndex &&
                decryptKey[i] == plainLetter)
            {
                alreadyUsed = true;
                break;
            }
        }

        if (alreadyUsed)
        {
            cout << "\nRejected: plaintext letter "
                 << plainLetter
                 << " is already assigned.\n";
        }
        else
        {
            decryptKey[cipherIndex] = plainLetter;

            cout << "\nSubstitution accepted: "
                 << cipherLetter
                 << " -> "
                 << plainLetter
                 << "\n";
        }
    }
}

// CREATE ENCRYPTION KEY FROM DECRYPTION KEY
void create_encryption_key(
    const char decryptKey[26],
    char encryptionKey[26])
{
    for (int i = 0; i < 26; i++)
        encryptionKey[i] = '?';

    for (int cipherIndex = 0; cipherIndex < 26; cipherIndex++)
    {
        if (decryptKey[cipherIndex] != '?')
        {
            char plain = decryptKey[cipherIndex];

            int plainIndex = plain - 'A';

            encryptionKey[plainIndex] =
                char('A' + cipherIndex);
        }
    }
}

// VERIFY SOLUTION
bool verify_solution(
    const string& originalCiphertext,
    const string& recoveredPlaintext,
    const char encryptionKey[26])
{
    string regeneratedCiphertext = "";

    for (int i = 0; i < (int)recoveredPlaintext.length(); i++)
    {
        char c = recoveredPlaintext[i];

        if (c >= 'A' && c <= 'Z')
        {
            int index = c - 'A';

            if (encryptionKey[index] == '?')
                return false;

            regeneratedCiphertext +=
                encryptionKey[index];
        }
        else
        {
            regeneratedCiphertext += c;
        }
    }

    return regeneratedCiphertext == originalCiphertext;
}

// MAIN
int main()
{
    cout << "============================================\n";
    cout << " MONOALPHABETIC SUBSTITUTION CIPHER\n";
    cout << "============================================\n";

    // Read plaintext
    ifstream inputFile("plaintext.txt");

    if (!inputFile)
    {
        cout << "ERROR: plaintext.txt not found.\n";
        return 1;
    }

    string plaintext = "";
    string line;

    while (getline(inputFile, line))
    {
        plaintext += line;
        plaintext += '\n';
    }

    inputFile.close();

    cout << "\nPlaintext loaded successfully.\n";

    // Substitution key
    //
    // IMPORTANT:
    // This is an example key.
    // Use your group's assigned/random key.
    string encryptionKey =
        "QWERTYUIOPASDFGHJKLZXCVBNM";

    // Generate ciphertext
    string ciphertext =
        apply_substitution(plaintext, encryptionKey);

    // Save ciphertext
    ofstream outputFile("ciphertext.txt");

    outputFile << ciphertext;

    outputFile.close();

    cout << "Ciphertext generated successfully.\n";

    // Frequency analysis
    frequency_analysis(ciphertext);

    // Word frequency analysis
    word_frequency_analysis(ciphertext);

    // Pattern analysis
    pattern_analysis(ciphertext);

    // Cryptanalysis
    char decryptKey[26];

    for (int i = 0; i < 26; i++)
        decryptKey[i] = '?';

    cout << "\n============================================\n";
    cout << "       ITERATIVE CRYPTANALYSIS\n";
    cout << "============================================\n";

    cout << "\nUse the frequency, word and pattern analysis\n";
    cout << "to propose substitutions.\n";

    interactive_cryptanalysis(ciphertext,
                              decryptKey);

    // Display final partial/recovered plaintext
    display_partial_plaintext(ciphertext,
                              decryptKey);

    // Create encryption key
    char recoveredEncryptionKey[26];

    create_encryption_key(
        decryptKey,
        recoveredEncryptionKey);

    // Display recovered key
    cout << "\n============================================\n";
    cout << "          RECOVERED SUBSTITUTION KEY\n";
    cout << "============================================\n";

    cout << "Plaintext : ";

    for (int i = 0; i < 26; i++)
        cout << char('A' + i) << " ";

    cout << "\nCiphertext: ";

    for (int i = 0; i < 26; i++)
        cout << recoveredEncryptionKey[i] << " ";

    cout << "\n";

    // Verification
    string recoveredPlaintext = "";

    for (int i = 0; i < (int)ciphertext.length(); i++)
    {
        char c = ciphertext[i];

        if (c >= 'A' && c <= 'Z')
        {
            int index = c - 'A';

            if (decryptKey[index] == '?')
                recoveredPlaintext += '_';
            else
                recoveredPlaintext += decryptKey[index];
        }
        else
        {
            recoveredPlaintext += c;
        }
    }

    bool verified =
        verify_solution(
            ciphertext,
            recoveredPlaintext,
            recoveredEncryptionKey);

    cout << "\n============================================\n";
    cout << "              VERIFICATION\n";
    cout << "============================================\n";

    if (verified)
        cout << "SUCCESS: Re-encryption matches ciphertext.\n";
    else
        cout << "NOT VERIFIED: Some substitutions are missing\n";
        cout << "or incorrect.\n";

    cout << "============================================\n";

    return 0;
}