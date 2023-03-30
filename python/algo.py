
def isPalindrome(x: int) -> bool:
    if x < 10 and x >=0:
        return True
    if x < 0:
        return False
    chars = [a for a in str(x)]
    l = len(chars)
    i = 0
    j = l - 1
    while i < j:
        if l[i] != l[j]:
            return False
    return True

if __name__ == '__main__':
    print(isPalindrome(-121))