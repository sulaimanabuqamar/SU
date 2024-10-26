from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMessage
from django import template
from django.core.exceptions import *
import studentsunion.settings as settings
import json
import random
import os
import datetime
import sys 
from threading import Thread
import time
# Create your views here.

register = template.Library()

logo = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAVUAAACgCAYAAAC8JP8wAAAACXBIWXMAACxLAAAsSwGlPZapAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAEafSURBVHgB7Z0HfFRV2safSe+910nv1ADSUaqiKIqggCj2tjZ2dVddt7m77uraKyqiICgg0qQjHaQESO+9956Z9O+8J0T5lJJ7c5kwk/PfX9QFJsxM7jz3Pc/bVP6jlnRDIBAIBP2mq7N7qREEAoFAoBhCVAUCgUBBhKgKBAKBgphA0C9U/J+/2NLd539FIBAMToSoykDFpDPAxwlqP09YWpjDzIQJqUoFrbYNTS2tKCyuQH5JHUQGUCAYfAhRlYBK1Y2hYV6YOmE4YoeGICwkABbm5jA2Mea/39bWBo1Gg5yCUqRmFiGvoATrtx5FS5uQV4FgsKASJVWXhw7zZqbG8HG3wat/vA9qXx+4uDjCxMSEiezFj/rd3d38S6vVIiMrD+u+34N9x9JQUdfCfh0CwYBDV669rQXMzMxgYtzNvoz4tdnR1Y3OTqC2vgkdHV3itCURKqkSkeoVcLI3x8wJUbhv4WyEhgT36TEktvRlZWWFoTERCArwxdjY41j+9R5kFVRD09YJgWAgYPEBQgN9YGNlisW3jkN4WAAcHR1hzk5cFAhoWjRobGrChi37cOxcPjttVaKBWVqCviMi1csQ6G2PB+6ahptmTIS9vT2MjOQXS7S3tyM5JQ3f/XAY67fHQdvWAYFAV1iaqTBmeCgmjonAzdPGwc7eDhYWFpc8bdEpq6GhAXsOnMLBEynYfywR7Z0iCXslKFI1dvAe+lcIfsPEUaH43X03Ydb0ybC1tbnkxddXjI2N4ebmiqFRQbA07caJsxmiUkCgE5ztTPHCY7fh4XvmYMJ1I9j1bAtTU9PLXtNkb1lbWyMqPAijh4XAzkqF7LwSNGtEMHA5WLC/WYjqr6DM/rRxEXj1hXsxbGg0v7gU+97nLYGI0ADYmncjK78ULZp2CARXAwtzU9w8ORxv/u1xTBw/WlZwQKczWxsbjBgaiRkThyAnJwfVLDfQzvxWwW8RovobujEq2gd/ee4e+Pv79js6vRTmLDkQEujLjmTdSE7LhaZVXKACZbG2NMGTS2bi8fvnwdPTo1/WFUGPd3BwwLCoQNhYqFhuoJIFBG0Q/H+EqP6KUdF+ePHpuxEZEdbvi/CyMK02tzBHkNoHjjbmSEjOYMkrYW0LlMFY1Y2n7p2J+xffynIBdooFB/R96PvFRAbDzcEcew4n8vpswS8IUb2AGSzD/9pL9yMkOOiqRagXQn8HJQrCQtTwdbNDdn4R6hq1ouRK0C/cnSzwjz/cjbvnzeYZfaWh65bKsMJCAmFv2YWk9AJ20hI+ay9CVM8TFeyOvy1bhIAAtU4E9ULIs/X19YSbkxWzAnJQ1ySOVAJ5RAW64I9Pzsf068cz4TPF1YROcsGBfrBmup2UJoS1FyGqjAAvO57ljx05lGfoBwISVrWfN/y8XJCQmIr6ZpG8EkgjOsQVr/5xKcZdN5Jl9nVTfk6RMOUG3J0ssfdoMgRCVBEd7IYXn5yHyROvuypHpb5C0TEJa4C/N4aE+aKktBzlVY3o7BJegODyGDH/9MEF1+NfLz6MwAB/nZ+06HMTHRkCO/MOnEspQOsgr78e1KJqa2mEvz57F8aNjeXe5rUAfSA8PNwQGeyF5qYGpGSXAqKWVSLdcLVnH/RQD17sPiTCH2ovR3S3a6Bt60R7p6HcqLrhbGeOx5fchCcfvIPXng4kbi6OaNU0ICO3bFCXW5GoDso2VQdrEyx75DZMnnQdL4K+liCvKiwsBMueWISGhmbsPpYhMqxXwMykG54sQXPfXTfCx8cb7i4OcHG2g421FX8/NRotqmvrUVJeg1r27x17juLQ6Wy06XGHUKi/M557+DbMmDrx6laq9BEPD3csunMW2tta8dWWOAzmYGDQtak6syjmmQdmY/7cWQN65O8L5eUV+HjFRqzbcQrNWpEIuBArC+ZDeztj0ZzrMGPaRN6/3tdGDZomRm2Y5F+v+GYXCkvrUFpZjybeiHFti4GtlSnmTB2C55+6j5c3XUt0dXWhsbERf3vtE2w5kIyOQTjiYtC1qZL/9OSSGVgwdybvbLrWsWaRVkSIH4xV7UhMyYVoYukh2MceC24Zi2WPzseE8WNgY2MjKVqjhCTdUL29PTFt0iiMjFHDw8UGXe2taGxuQWv7tfdG09jJMLULnrx3Fh66d+CP+xeD7CuevAryQ2lJCQpKapjQYlAxuDxV9mqXzpuER+6be01ekBeDLlLqv44IVbMPfAuSMwqYJ4jBC/sZTo4NwCvLlmD69WP5LIX+HH3psebmZvBwd2PJlmCMGhaKEVGBMDdqZd5g+TUzm0GFTtwwJgh/ff5+TJ4w6prJAVwMumYdHewQGuiN1LRMFFc0YjBBojoojv9WlmZ4/J6ZeGDRbFhaWkIfoSlX23YewP8+2YSiiiYMNmwsTXE3O+o/cu9cuLg442pC73UJi7RWrN2NUwk5yMgpGZBTgomxCgHejvjd0tnMO51wTYvpr6ExgiUlpXjwudeRllszaOayDpLjP4tQ75iIu+Ze3+/xfQMJHVlDgvzh6WKLpJQs1DfTjMvBkQwwM2a2zX03YunCm+Hk5HjVy4bovaY+9/GjY1jk6g9TlghrbGhCfWOLzqJXE6NuzL9pFJ5+aC4mjBvFu5j0CfoZ0QCXYH93pGcVoKJ6cESshn/8Z69w+thgPPvYfJ6dHKjifqWgGwINvPZ1t0Nmdh6q6jQwdGG1sTDCY/fMwL133axoH3tfoOvFxcWJea6hGDkkGBGB7sjNy0NjS/tVFVd3R3Pmnd7IrSq1v5/eXre8RNDdFVGhfjgdn4na+mYYOgYtqmamRrjl+hgse+Iu+Pr46L2g9kLCGqD2RWxMACorK5FTWAVDFVZfdxv84ZE5LLE4C7Z2tjovbCd48sXCHF6ebhgSHYpbZozDyAgvaFqamE3QiWZNq2LzGizMjDBjfAT+/eL9mD51PE+mqvS8nI5Pt7KzxnVDA3Dop0Q0NBv2FgGDFtXhEZ544cmFCAoK0Nsj/6XgyQBHBwyNVKOsnAlrQYXBDbymCPWVZxdg5tSJsLaxvibEpWceriUCA/0xgVkDsUMC4Oxgg9raWtQ2aCEXemV+HnZYeOs4LHt8IXx9vQ3qmqVacEoOe7tYITk9F/VNhiusBiuq7o5meOvvTyAiPNjgBLUXel12dnbsWBqC2poaZOaWwlC6Wi1Mgd8/ehvuvG0mS86YX1PR2oX7x3y8PTFqeDhGjwjj0/VzcgvR0krlGVKebzeGh3rg5WcWYc5NU/jPVN+j04tB8wjcXJ1hZ6lCYlo+Wgy07trgRJWuRdor9cZfHsaIYdEGeXFeSG8yYPK44XCw6kRyRhE0/bxYVedj3r5+Gf38uF/+2R/UXvYsQr2LCeoMvbBsqOGAxOK62Bjcecsk+LpaoLqmDm1tHWhj9sCl7nN0aXo4W+O+udfhX688iZBg9TXX3ac0PaMuA1jEaokDx5MMsjnA4EqqfD1s8eLv5mPq5Ov0LlvaX1paWrB1x4/4csMBpOZU/j+fj4TSwlQFLzdb+Hi6/vzrxibGsGQXOtVq0qdfZURedE9X0oU3pItJJf22CXs8/R4NfsnMK8VPZ3P6ZUN4Olviny/cgymTxurtCYPKsYpLSnEyLgmnz2XhZHwG8kobcOG7SD+P64b4YcmCmZg0biRv8hhMdHR04N1P1uCLdQfQqDEsZaWSKoMRVVV3Fz5/4wlMGDti0AlqLxqNBpnZBewDnYj1W35EdHgAhkaHsUjKlR1XzeBobwNnRzsuuCSKvQOHSRwJ+v+/iNkFInBRnVT9/Ot19Q1Y9vI7+CmxWLao0iT5F564A7fdPE3vk4pUo9nZ2YmmpiZk5xbh1NlkrN10CAXlDVCzG/9tM8fi1tlTWALVy2ASqFKpq2vA56s3YfmafTCkUawGI6quTjZ49flFmHnDOAh0B4lHc3ML3nzvC6z4/iTkHv+9XKzZCWMBZs+aZLCWDc0bKCsr5wkbBwd7g7em+kJjQyM++mIDvt583GCSVySqej+lysvVFg/dPRVjY6Mh0B0kqDQ8Y/uuw9i2PxFyBdXRxoRFqPNw44wJBi00dCLw8/OF4BdsWD7gkftu5yMZV6w/BEMpDdRrUTU1UWH+TSNxC4tw9KWf31Agq2H3j8fwxvJNqKqXtwLGzcGMj6+7edbkq3IMpklU9HUhNPBDX1uVDY2eRYL2eHjJbaDZ1qu/PwxDQG9Fle5p08eF4e55umldFPwCRalHTsTj1Xc3yF794u1uh0fYCWPW9ImKCyo9v9zcfBw7GY+vmZfZeMFzdHG0wr13XI/xY2PZdWPf53GBgquHm6sTlsy7AYXFZTh4MgP6HrHqbUnV0DAvvPbKo/DydBeCqkMoAROfmIrn/74clXXyfDArcxWeuX82Fs6/mRfTK/ncmhqbcPDoObz18Tf4ctMJVNW28C6e3q+yqibsPpyAvMJSeDha8jZUIawDS0/EasvbgM8lZaKyRn/bWfW2TtXL1QbPPngLhsVEGGxx/7UIRYBp6Zl486NvkJpbgy4Z/ZlW5kZ46v5bcN/COYqKGT230rIyrP1uF95ZsQ1peVWX+dMq3oWWkV0IE1U71H5e1/zAckOHt7M6OMDF3gLHTydB06afg1j1UlSNWFA6Z9pILLnrZvFB0DFUC/vpV5ux/WAK2julX/TebrZ4eulNmD93Bq+PVQouqKVl+PTLTfjy+6OoayQf9cqnl/LqRsQlZkHV2YZAfw+D6LXXZ8gG8mc3OFtrS5yOz+DNE/qGXoqqr4cd/vXi/Vd9pqbg/0NF7bTb6Y3lW2XNFnW2Z0mpB2dj/h03wUrBRBGt8CgsLMbKtdvwxcZjaOc1j30XRso8nzibySPokABv3vUjhHXgIGEN8HNHfW0NUrNK9G6jMImq3p2dbxgbxsf4CXRLdXUNPvxqOzq7pV8yNByFVoHPnTNT8VbMgsIiLF+1Get2nMYvTbPS6GKP++zbA1i35SAfjtLdPVhGKl+bUCXPkvkz4eqon1UaeiWqpsZduGHSGIPvkb7WoGP/O599h6yCSkiF/O9//XEJ75RSstONItTSsnKsWrcDG3acYRl+eWVdvTS1tOKDr3bgy292oqqqmn9/wcBAJ4WAAH++flsfDw16Jao0Hs3P2wMC3UFRW2p6NuISstl/S7vCA7wd8NJTd2L2zEmKlk1Rlr+kpAwr12zFivVH0KqQ99bc0ob3v9yJDz9fh6KiYv73CAYGEtYpE0ciwt8J+oZeiaraxw22djYQ6A6tthWHjp9j2XJpUaqnswWef+x2zJw6QfE6VIokv9u2H+u3n0K3wpcwWQHfbo/D6vW7+IpwYQUMHI4O9phwXTTfJKtP6Fek6uMJayvRDaNLqmtqsf/IWUnJKXcnK/zhsXmYdv04xcum2trasXnHEXyy5gBq+jEY+nLQrM/Vm09g5Tc7UFpaKoR1gDAzM0d4iB/srfTL7tOrqmfqFRZ1qbqluLiMeanV6GtG3dbKDI/eM5Mf+ZX0vukoThHqD3uO4V8fbsLV7rpp0bZh+TcH0dnRgSV3zYKPt/egnSg1UBgZqeDn5QYXJ1vUNddCX9ArhTJjH1JR7qI7KFmTnJaJFgk5oFtuGILbb75e0aQURYoVFZX49vvd+PCr3dBlG+OarSfwxdofuMcqIlbdQp91NzcnODvZQ5/QK1HtXWUh0A0UHaZlFvT5zzvZmGLxnTcquhKEhKyurg7rN+9jR/4fUVXXBDnYWpvD3Ez6wUzT2oF1P5zCZ19v4Q0GQlh1i5WlFSwt9MvyE03PgktCBf+JGSV9+rMkofcumIaQYH/FBJUiZaob3bLrGN5csRM9MYD07z1hZDDuvmUMEtOLmECekOzFtmg7sWrTSebn27LXOAPu7u7ChtIRtNvK1Ex4qgIDgVYw1zf3razIiGVonR3tmdgo4ztSRFhbW4dNO1lSavVeyDpUse8xLMIbrzy3mO+AmjihiY+L/GD1fnR1SxVnFb7aeIR5rO24Z/5M+PgY1sbTaxcV/58+IURVcBm60NfDLuVwLC3NeHKhv5CgVldX4+v1O/HptwfR1CKvsJ8mmb341AIuqL1LEu9ZcDOam1vx7fbTaNZKG1tIySuaUt/c0oIH75kDtb+fENarjD66fUJUBYpAdfJaJlIkiP05/tORv6mpGes27cO7X+xCp0zbf/QQf7z0u/mIjo74+fn0JD5c8dgD82BlbYmVGw6jSSNRWJnHunbbKbR3dODxpbfzaf6iKkBwIUJUBZdEijh2suN0bX0jF8X+RG/19Q3Ytvt4z1FblqB2Y1SMP15ZthiRYcEXfS40jOeBxXN4FL78631o75J2E6CGg237k9mNRIVH770FQUEBQlgFPyPOLoJLQoX7TrZ9v+9+uW43UtKyIJfW1lbs2HcS//loE8qqGiAVyu7PnhKDv/9hCaLCQy4p7nSzcHR0xAOL5uDBu6bAykJ6IoSqAjbuOYv/vP8t0tMzRVWA4GeEqAouCRXvRwX3fSJYZV0bdu8/xQewSBEZim4bGhp5HerL/13FPFR5nVJTRofg2UfmIZxFqH2JsmkNz31334xFc8YwYZUTaaqw76d0/Pm/K5Gcms4Sewa0a1kgG70SVfrwiYhAd1Ck5+vpJukxazYfxZFjJ/hiwL7+rKhT6psNO/Dhlzt57710ujEpNgDLHr0TQYFqSbYFeaz3L74Fi24dyysYpKNCXEopXn9vLRITk8V0K4F+7agaNSQQo0dECv9KR5A41TU0YOf+M30uQaJjcXp2EVwdLODr43nZVlW+oC+vEBu2/IiPVu9FbaMGUutQrSzMMGtSNH7/+N0IDQmQnCSjP29jbY3osACYqDqQmlWEtnbpwphfWouMrDwE+rrA28tDNKkoBFlCuw+eQXZBOfQBvZv8H+DtiAnXDVW0BVJwaUgYTJmvevT4aVTX933JX3VdC06eSYWZiTHUvm7MmzX+fyLTwTLnxSVlOH4yER+v3IS1P5xCWwdFiVKFqBu3TB2Gl55ZBD9fb9lCRo+ztLJkiS1/lrltR1J6gQxhVfGlgifikjAiKoAvFBTlVv2HVoyTqOYIUb062FsbYdqU0Ypu4BRcHiMmOOkZeUjNLoUU0dO0diEuKQep6TnIyc1HU0MdiouL2X8XYN+B4/hi3X6s2XQQabmVgIzibhUT1BvGBONPTy2Cp6cykSHtPAsN9IFRVxvOJGbLaBAAGprbkZGRBT8vJ77pVwhr/yAbadf+OOQWVkAfIFHVq5Kq4tIa1NXWw8VZ/wbX6itUMD91SiwOnEhliSiJ7Z2aNvx4PBWHT2XAkh3TqS+A4lHq1KJCermDUSzMTTBlVAieZkkp6mxS6qjNqwJY8urehTfDiH0yVq4/zCwJ6Wu4z6SX4x9vfY1lj2gwbepEYQX0Aw2LVLVaDfQJvYpUaW/7iGhfhAYHiAtVR9D77GBnjazsPOZrVUF6nlDFkjfdaG3rgJZ90b/b+XBW+T+/W6cPxx8eny85KdUXuBVgaYmwIH/YWABpmYVo1krP6lfVa3HkRAIiQnzg4yUiVjnQtZaTk4/Nu44z+0k/hFXvFv9RZjg9I0dUAOgYKj1aPG86S+got1ZaFuznPuf6GDz/xAL4+vpc1Rurg4M97rxtBh5ZNA3W5vL+ntqmTvzhb59i9/5j6OwUVQHS6UZVdT3qG5uhT+jd7fPAqRxUVVVBoDsoyoodHoN7bhuHgYI81FHslPLg4tl8StTVPqnQ96cRhrOmT8Di2ybCwlTe31fJIta3l2/E6TMJIhiQCCU0s3KL9CZK7UWvjv9Ea2s7XOzNWaY2UNFVHYLLY2RsBG9PZxQV5CO/pBa61AcS1Cmjg/GX3y9BRESozqwfPoTFxhrREQEwRjty8suZFyxtVgBBorD34AkMCfeDl4ebsAL6SHNzM77+bhfS86qhL+hd9p+gzZnV7EgwLNIfbm4uwlvVIXYsaeXh4oBUZsFU1urmSEaCOmFkEP783D28x17XgkTXF1UFDI0OQUdbEzKyCqFpk36UJy1OTM6A2tuV1+8qMc3L0MnLL8Kna3azXEr/1o/rEr0UVaKusQWmxh0sWlXD2toaAt3Apzy5OiHI3wMn4pKv+sVuzHRn+rgw/PHphQgODhywCI9eN9VGB/h7QdXVivSsYiaS0oW1tkGLswkZiAzxho9YtX5F0jNy+SQxfUJvRbWTZZMTUgpY1GSFsGB/RRfMCS4PdbNRpDV2RBgSUzPR0NCCjk7lvQB7GzM8eNck/PGZpfC6RjqUrK2smBUQBBOjdqTnlEAjoyqgvknLstlH2fsXAjcXZ/Z+CivgYpCfunXHARw/mw1d7iTrL3orqkQ3e6PpKBYZ7MGLrEXrqm5xcXZEbHQA2ltbkF1QhvYOZYTVWNXNh7g8dNdUPLjkjmuq0aPXCoiJDEZzUz2SUvMkre7uhZoK4s4mw8/Tkd2gPMS1+ytofsLBwyfxxidb0NLat80T1wp6LaoE1T1WVdciyM+FHUtdRAJAh/D6VQd7RIWr4c/EobqqHJU1zfxmJwt2NbrYmWDpvIl4dOlcTBw3kgvYtQidjPyZGNpaqpCUlne+xVYa9U2tSEnPQXiwsAJ+TWpaFl59axVyS6WPfxxo9F5UmQvAMtE1SE7Nhq+nA3y9PYWw6hB6r21tbBARFojZ08djyphQliVvQ2e3EY84ta1tl6wSoNO8vbUZEydXRIW444nFN+D3T96N6TdMgIe76zVf2WFra81uKEFwczBHamYBGlukVQXQ21JTr8W23ccwgkX8Xp6iKoDIyMjGM698gOQc/cn4XwiJqsp/1BKDKJ4L83fCqy/cg2FDY4THOkBQHSZNFSovr0BaZh7S8ypRW9eIxsYmPhiDCuAdHR1gYWEOM1MTBPo4YeTQcDg7OzGRsuUZcX2r5mhoaODe37/e34jmVnkfJT8Pe7zy3EJMHj9y0F67dO3QdfPKf1Zg99E06Ctdnd1LDUZUiRERXnjuodswZsyIQXFxdnZ2orOjx3OiNb7XmiCRN9bW1saFtuP887SwsOBTqygqo2hU30viSAxop9bKNZvx0eo9zAOU/nGid8Dfyx4vPDYXM6ZNGnQeKw01/2HnAazedBjxacXQp8TUrzE4USW8nC3xxNLZWHD7jQbVHEDCVFNbj7yCYhSXVqKgsATlFVUoLquEkcoIzk728GZHSB+WKfdwJ4/ZEQH+PtyXFMfKq09jYyO27znEB23ny/QCbS2A9/75BPeTB4Ow9m7NXblmCz5es58l/fT/OjVIUSUcrI3xwhPzMe/WqXofsba3t6Ourg4r1mxHZk4R4lnGua5Byy5A1W+SQvQrxkbdMDc1gtrbBaNHROD6cTEYHTuUi6tolLh6kEBQB9CR46fxz3fWo7CiCXIgK+DlZxdi/OgYg67BpverpKQUX36znUWox/Quy38pSFT1OlF1KbTt3TiTmAVba1NEhQXobaRWX1+Pbcyve/2jjdj241lkF1ajRdt1fs7nxQRSxX+vnV2flbUtSEjNx8lzWcjOK8aQCD8+fUlErVcHPtCb3cAD/H3h4mCBM/HpaNZKFwqqCjgdn4FgP1d28rj2E3Zyqa6pwX/f+Qobdp2Fps0wBJXQ++z/5dC2duDYySS0tjQgPMSfCYqF3kRq5JVmZuXg9Q/W4P1Ve1Fc0cB+WJcS0ktDkWxDsxbJGUX4dtM+aNl7Eaz25r7mYBRXio7ova2srGJWSi1LotXxRBONJjQ3N+v39UGPp/c1JEgNH3c7JKflcJGUSlNLK3buP4VhEb7MxnGGmZnh5Afo/U9Nz8ILf30fe3/KuSqNIwOJQYsq0cmOyAmpuTAz7kKQ2hNWVlbXvLB2tHfgwOETeO+zjSwLmg6lBolRLeWpePYhr62Cp6vDoFv3QYJKmwc2bt2LVev3YPven7D7wGnsP3qWz4oNDfKFBbNIlPAy6X0NVPvC282WRaxpaNRI77yiE8eZhDR4udqx7+VjEB4r5QVOn0nEa++uwcmkUhgiBi+qBAlrckYhjLrb+QeHhPVapampCT8ePom/v7kGqbnVV2ESlAqZeeXIzM5FVKg/j4IGCxSRfvD5Rny69kde6lVY1sBPAIVl9UjNLGZ+dQFGDw3m14dSwhrAhNXD2YbXUdfLmJPQ2NLGgwJqbnFxtL9mmyH6AlWBHDpykvnN3yI5u1KnU850yaAQVYKWuJ1kUVpebg5GDQvnCYBrKWKlKIqyx+u+34UX/7MG9S0dV+2io1nJxRWN2H/oBCZdFw1HB3uDT2BRjewnX27Cp98c4H7zr20Uek/yiqqQkV2EQF9XXkmhhJdJwhoc6IfwADekZeRxn1sqtO1iy+6TcLQ1Zactb71LONK1TSVTe/cfxTN/XYGKOq3BCioxaES1BxWyC1iip6kWIQFesLe3uyYuTrroamvrsHHLPrzzxU5o23RzxTVpOlFeWoKYcH/Y2dkatBWQkpaJD7/cfoVhxyoUlVajsLgEUcHevElBqYiVVlb7eNjh+KkkWckrem7xyTlwtrOAv68798T1RVgbGhqx6Yf9ePPTbahrlj6LVt8YZKIK3huZmVeBqooyRIWpubAONHQX37BpF95buYMdEaV7b/2hlB1/KUIeERPMKwMMNWLd8P1ObN2f1Ic/qUJJRR2KS0owNMKPT/5X4mZD38Pf1xuuDpZITMmS3NJK0GmL2mFNVR3MxvLjwnqtQx7q5199h4+/3icrStdHBp+oMijbSGuRT585h+HRweyo5zAgYkIRak1NLT5f9T3e/HwnNG26PxO1s3Nvdl4JLFhyOSYyiM8MNUT+/c4qlFX37UNNR9OCklrk5BXBz5t5mc4OilgBdI2FhQQgOtSbedoFKK+WXsfapGnHT2czYGdpDLWfxzV7I6QMf35BEd5470t8uu6oQZVMXYlBKaq9VNRokJGZhRC1J9x1vUGAfXBrqmuwev0OfPrtAZaZx4BBo+sqq2owflQkXF0Mc/X35u0HUFTe2Oc/T7e3wtIalJRWIIZFrA7sRKOEFUDXmKeHG4J8nREXn4Y6GeuveVVAci67EXYzj9XrmhNWak1OSEzF/z78BruOpvFE8WBiUIsqUcGihSyWCVd7O/OLXVe+YnNLM776Zgs+WbsfLdr+3sV7I1z5F29Ngxa25p0Yf90Ig7QASkuKcfxsLqSh4sJaUFiK0cOCeHJTKSvAy9ODWQEWOJeYIavcilZ8Z+SUwAQ9FS0krNcCdPqi7r9nXnoPp5KL2PPEoGPQiyqNDiypbMTxE+fg7+0EDxaxUlfM1RKW3qTUmx98hY/XHpIVoRqpuuHv5Ygpo4Pw+4dv4bubHl40AzdfP4SFnS0sMuhkPq2WHe2l2QlF5Q24YWwEnBwdYWhYMv+R6lGbWqSWNZGwViM5NRM+7g78RKOUFRAc5I9AXyekZuTK2haq0bbjxNlMdLU3IzjAGzY2A1vR0tKi4S26T738AVLzavhnazAy6EW1l0aWCU9iCQQb5lX5+Xjy0XRKQ4JaWlqG5V9twtptp9AhI0A1N1FhxoRILHtkLhYvmIOQkEAeQdGXh4c7Jk+IxXUjQuFgbYKSskrUN/VdRNo7OuBsb4nYYZEGF61aWVqgubEWCWmFfBWPNFQoraxHQVEpS+gF8uWHSlkBfix5pWY3yPikTFlWAHXMpWQVMWHVIGQAhZXmU3y/dTfe/mwLcopqoc9TpvqLENULqGcX9bmUHFiZdmFIdJjiVkB9fQOWr1yPVZtOoFWGcW/GBPW2acOw7PGFiAgPuWhETR92JydHRIUHQu3jgtT0HL5sri90ssjW2dEeUycMM7h+c3o9TvY2qKwoQ16x9CiKxKusoh45+SUYw6wAGxsbxawAP18veLpY8w21tQ3ShZUSr1n5ZaiuqsSQqEDY6HgIC1WPbNq6E298th0lfIjM4B7aI0T1V7RoO3DoZAZsLTrYkcpPkX5wPt6spgavvb0Cq7aclhEp9Rz5l9wxES///n44Ozte9jn17lGiNkkvFxucPpfBs8Z9wdrCCLEsGnNxMaxOKxp+TUm4IZFqFBUVIb+4WpawkhWQkt7jwbu6OCpmBQSyay0q2AspafJWf9NNOimzFJVlxXyAkC2Lpq92xErXdVlZBT776jt8sHo/i7T1Z4301USI6sVgF2NiWgHsLY0QFODbr9ZA7qHW1WPN+u34evMJWUd+ExYQTR0fhX/86SFJCQn6UNnaWCEjMxuZ+VV9ekxHmxbjYiOg9veBoUHvB0WYAb5u7D3JRXlVI+SMky6tqEN9bS0iQnz4ji4lIlZ6buTX2tuY4vjpFGjbZGwTZOQUVqGztQkRobS63eqq5gaqKqvx2ddb8PWm4+ymPQgzUpdAiOol0PI7fwFqKssQOzxK9oR6mq+5ftNu3m/e2CL9wjNj1t208RF4/qlFsvr0qY/dzdkaG344jj4dy7o7cf34YQgJ8oMhQgJI5VGhQd6orKzg9ajdMiLW/JJqlJWWIiLYG/b29opZAcGB/rA2o8x+kawGgS6mxVn55WhpqsPwIWFXpUGgJ0Itxwefb8CazccGpL76WkaI6mWgne50pKoqL0RYiB9v5eyrsPYOLF759Wa8u3I3GnjWWZooq9iRf/q4CLz47D28G0eOqPPojHlsX6z9oU9T1dkpGdMnjUBYsD8MFbpBUpVHTJg/ystKkFck3WOlP59bVM0HpYQHesKV3fCUEtaYqFBu2yTREJYm6Ufqto4uJGeVoLaqHCPOC6uSEWtmdh7e+WQdfjiQyARVXkRtyAhRvQJd7B1Kz6tAZXkZIkP9+HHvSvQOR9m4taeXv2eiudSLuhvjRwbh3y89BC+v/m2IpVmc23cdQFX9lZMgKvbcJ46Jgp+3K28xpKwu/d30oTSkioCf12uH+qO2pgq5dGyWqKwUsZYyCyEzpxCB3o7s5+ShyHvUOzYw1N8FR04mc59fKhSxpuWUM2EtY0nLAEWqAqhLihbz/ff9tdi6P5GLt+C3CFHtA3SB5hVXobAgHyOHhHBf7nIXqEajxcYte/D+l7tQJyPSoJUoMycNwVMPzuU7pvpbvkPP9dDhn5BdXH/FP0uyUl3biGOnUrD7YBz7OoujJ+JRUlSI9lYNn5VgKCLbK6zRTHRKSkq4HylnelJpZQOPKmNjAvj3U2oIi6+PF2zMWdTJEmPNsuaxdiOnqBJN9TUYFhMCq340CNAN9uy5RLz3+WZsP0gzFMRankshRLWP0Gi43KI6JCWnIlTtAUfH346GowhVo9Fgw6Y9eP2TLefrDqVdfMYqEtRo/OGJBczX9FdkvxbNsfxs9WZU1PWlXEeFsso6ZDNfruerDCmZRTgZn4sdB84hISGRRe3lzFKw5Hvv9b30ioSV6k5HDw9HRXkJsgqq+BYAqVTXNfM650A/F8U68+i5RYYHw5N54olpuWiQMY+1vaMbqTmlaG6oxtCoEFlWAAnqDzv343+ffI/TSQWyqlcGE0JUJUCXEs0hPZeUDldHaxZJeP4sKj3tefUsKbULbyzfhiat9CM/CerUceG8Q4qiFKUEiwZfv/7hRr4oUB4q3hZJ62mosPtYXCZOxiVw/zXQz/OqdqDpAnrulCkfMyISDbWVyCmo4K9X4nfhA1JSM3Oh9nTko/6U8liDAv0Q4ueM7Lwi3lYtFTppJbPcQDVLukaGqSWVW9Ec2i07DuDVt79FUWWLENQ+IERVBlV1LUjJyENksAd8vD35BUotemvW/4CPvt7HIgrpWVs68k8eHYLnn7wb/n7Krc7o6OjA7r2HWFJBuSMbeYlV9VqcScxGe5sW/t4u7INqe9WFlQZ10JhESgDSh538XiUFnbroyH/UNtczESqRFbFW1jQjMTUXwyJ8eK2vUsJKN9lAXxdmM2SxqJimbUl7zfRSsvIrWGKuFGNGRvbJCqD3eOO2A3h/5XY+WFrQN4SoykLFjvZaJKTmsajEDvZ2Nvhuy268+fkOWWUwJKjTJ8bgxafuRmCgv2KCSiJEowU//nILslmGW2mo4DwxrRD7j5zi3Vs+3h6Kd6H1LuorLavAxs178Of/fokV6w7g6+8P4uTpeDjZWcDL0+1nn7c/9EasVIrUWF+FlKwSHuVJpaa+BfGJGVB7Kxux0uuk+RSpzGOtrpM+K4CizKz8StRUUlVA6CUXYdJ1Q4sRv9m4F298upVbG8JD7TtCVPtBDbvY4hKzkJ2TizWbj6JJI/0TaGxEdahR+Nsf7uFZfiU9yqqqaqxgXiqVvlytTG0HM5trWNR6Mi4Rvl5O8Pf1VHRBHSX9jhyPw3/eXY3VW05xMWlq1vKv/JJavnHU0dqYr3K2srJURFgpYh0xNBzN9dXIzJdjBfScZlLZacbT2QoBaj/FqgL8KGL1cUJSWo4sYaVEXEZeBWprKhAVqv5NVQCdbAoKi7B63Xa8vWLX+dcuBFUKQlT7SX2TFinZZWhtl35UNDHuxqyJLCn1+AL4+HgrLEYa7NxzBJ+vP4BaGYM6pEIdNdRiGeDryuwLL8WO5PGJafj3u2txNo02b/72e5JPfDoxkw8UCQ/xU2ypo7mZGZ+foOrUsON8Ift7pP98q+p6rICYUKpjdVFsCAtFv2oWsSYkZbCfLR3LJVoB7LXkFFagsqIcscMjfrYC6FSQnJKGz1Ztwaa98eyaFiVTchCiqgjSBYSSUrMnx2DZ43dBrfZV7Njc23RA0d3f3/mOR0y6ijTIEsnMzMaoYaF8PkF/aWtrx6dfbsCPP2Wx13Xp19DGbmgJGUWoKie/MEqReQ30eIp8h0QFw6hbi/jkfBnCquIVIGeZ6Ku9Hbj/rtgQFu6xOiM9s1DWrACqCsjMreClcmNHR/NW7HPnkvDaO6ux/1QONK2DZ1K/0ghRHQDIQ519wwj8+8+PwN3NVdEEDzUd7N1/HK99tPn8ug7dHt0qazVwtDPHUCZG/S0Ho6qFf721CvUtV/6A04StlKwydGrrfl5DroSwkthEhwdB1aFBanYxi96ki01NPXtsZj583W15wkmpcisSadogEJ+cyYeMS6WnK6wKrZoGmBur8Nby9TieKM9HFvyCEFUdQ9OmZt8wFC8/twROjg5QEqon3LnnMN5l2dqC0oGbaZmeU4KIAFeo/X37JWzUvfPJmt19LwVjf1dqNk3D72CRnCvsFKpIoI60sGA/mHS34VxKPh+1JxVex5qWi6Hh3twKUCx55eUOL1dbnElIY0lS6a3QVH+dlVeOk/Fp7L2rEiVTCiBEVYfwLP+ESLz87L3w8nCDUvTuVT909BT++e46Xks7kMmF1tZ29qXBuNjIfnmcjY0NWLV+b59mFvRCgpecUQhtSyPCWMR6pe63vkCPp0x5DBXPm3TgTFIOj4wlfhfUNmj4MGofdzvFIlb6HjRRLDTAgy8TrKiRfjqh6JuiaSGoyiBEVYcEsaztP1iWPyDAT9EjPx2Tfzx0Ev/5cCOKK+WXv9BTsrMyRoC3M5wdrdCq1cjcMaSChol8ZIgXAvoRrarY/zZt34+GFmlHbvILacK/EYssw1mEqcRiPHo8Raw0Us/cqIN3mWklDxpXMY9bg6SUbDjbmSI4SK1gHasnhoT78DkEtGJbZOwHDiGqOoKi1McXT8PU68cpmuWnAu2DR0/jf8u38hIjufi52+DhRTNx99zJuH32BMycNALDY4IxLFKN3Nx8yWMLta1tCPJz46VJcl+viakJysrK2JG7gDccSEOFtJxSqLrbEaz24OtmlLiRkU8cwiJgU1Uni1jzeEmZVGrP1ziH+Dkplryi1+bi7ISwQBaxMv+W5hHAgAbg6BNCVHWEo7UJnntsAdzcXKAEvVn+w+zI/7e316Go7MrDUi6Gg60FJowMxN+fX4pZ08bxeQM0LNmNJdDCgtUYGh2MMcNDYWbcjuyCCpZp75uI0BplS9NOTBo7nGfR5cAjME9XpGdk86WEUqEay1QWUbZpGxES4KWYFUD985HhAcxraEY8lVvJ8Fgbm9twJj4DHs6WfOq/UhGrO/NrI9gJIT+/CMXlImIdCISo6ohJsUG47aYp3JtTgp4j/wm88ckmSfvsL4Sy0Q/fNQVPPDgP/heZhkUCQr/m7u7KJznR8OT4NCZSfcyA21oaY9bUMTxhJBea+uTt7oiMzCzmF0ovdqemh/hUllxqbeZWgBLT8HusADNERwTBxdaIHblLzieJpFHPhJWmW1madiEiPFixiJWGmccOCURWbgFLWFInnRBWXSJEVRewd3nKuGhMHj9CkY4pOvIfPxmP/328CbnF8rL8QT6OeOahWzHvtpl9WmJH0SYNri4vLUFyVin6glbbipunj4FrP/Zd9RS7u7NjrRdOnUmStQeJrINMluHu7mpFkL+HIhErQcIawqJ58qHPJmXLqu0kYY1PyYUT81hD2fdSqkGAthGEqN1xLjH9fK2yQFcIUdURY4YHYeyomH6Jau9owbMJKXj+n6tQKPN4FxHkjj89OQ9TJo7mLZl9EZjemk0bK3PsOnC6T22vFNHeOmM0F8X+QH83jdMLZ35hemYOi1iliwRZASmZJcyX6PFYlbICSFhpjxn5o/uOJsiyAlpaO3DiTDqszVWIiVQuYqUGDGNVF06fSxfdUTpEiKouUPUctSeOG8G7feRChf2Hj8Xh1XeYh1peDzmC6u5kiZeevB1TJo/lgiAF+qDSBtG62mqcTSnsyyMwd+ZonpnuL/R302T9QB8XpGVk8SYDqZCwnk7MRbu24Xy5lXLJK1oz7WJnjLSsIllWAIkeDaM2V7UhOjJUsUHXFqZGOJOYwRJX8iwigXSEqOoEFdo0LdxftLeT5y/SkX/P/qN4+7Ot7Mgvzyej3fLPPjgHs2+8XvaHliYYJSRl4lR8Vp8y8nfceJ0iokpwYfV0R0SwD07FJaKuSfoQcPrzNAKvTdPIIkwvxRoE6P2kFSiO7Bh/Ljlb1gqUFi1N/cqDl4sVglnCUImIlU4iZxPSkZZTBoFuEKKqIxqbtbybhgYOS/mw9B75T8bF4y9vrEVRRcNl++AvRbC/C55/9DbMnDahXyu3SYCoKP/EmdQ+rfhQUlQJeu/IChgW6c+nKRWW1kkuHaKIlcqtmhuppdVHwc4rsgL8EKZ2xgFmBbR1SLcCyJc9eTaNRZhdzAoI6bew0uPPnEtmCcZCiNp+3SBEVUd0sQipqaEWk8YO5TWTfYWy/AePnMY/3/tOdqeUl6s1XnnqTky7YQIs+iGovVRVVOHQ8d5I8fLQ8rq6ugbkFZaguqqGRbqd7IOu6tdwaXocVSQMDffjS/sy8ishFfI+EzOK0aFt4uVWUqbhXw5TUxPeLeXjZo2U9HyWiJI+IYw2lJ4+l4mutmaMGhHdL2Glk8XxE+e4XSNEVTcIUdUh1fUalozo5ll0OpZdDopQabfUvoMn8L/lW5BXLG/ItLOdOZ558BbMnjVFkcoDel4nziRjx/4zfYrEaPTdngNx2Hv4LA4ej8fBE0k4ejIVmRkZ8HB14OJKoiFVOEgAnZwcEROuRlJyGkoq5BS791QFtGobWSTvodj2ArICyGN1sDFFHK8KkG4FtDPRT2Ki7Me8+AC1/E0QNOD70NEziE8tEqKqI4So6hA6dmbmFMPWQoUQJqyXSxSRh3rs2E/421vrWZZfXlLK3toUjyyeijtunc5bNZWAhhgfPn4OB06k9+k5UQJG284sjNYuvlm2tKKeeZpliEvMw/b9p5CWnMxuNEbwYdGdVOHgS/uYRx0e5InMrFyUVEqP5KkjKoP5jY11VYiJCubJKyWgm4Xan0WsLubYfTiB/Yr0aJNuWmdZksnd2RLBgQGyItbq6mp8t+0IsouqIOpVdYMQVR1DCYxjcamoqSpn3qYJLMxM+QeQIsDe6DQ5JQMrvv4e763cfX43kPQPg62VKR6+ezLuWzSXlw8p9vxbWrDq213IKqhGf6CoqZllyTPyq7GLRbJFBblwcrCDo4M9P0L3FV6R4OqCYVFqFDKLIb9EehKPrICkrFK0tdSzZJMnSybaKeexBqrhYmuM5Ix8aGQkr2j4d9y5dLg4WMDX20NS9QhdT7Ry5tuttJVC+pofgTyEqA4AnSzRlJRRgmMnEljkWsQzvifPpuLYyWR2TI7D8lXbcPAUyyC3yqstpCP/A/Mn46H77uRJKSWHtyQmZ+DtFVuZEEExaLRfWk4F4uJTYWdpzFeySCn34laAoyMigr2QmpaF0io53jONDSxFC0teUbkVRcDKVQV4w8acfub58qoCWPLqDMvgW1sYSUpelZVX4p3lG5CYSZl/EaXqCiGqA4aKRyEZzNOLS8xGXEIWL1OilkrqGuqW+SGwszLDQ3dNwT133wobhYaIEL2zBv702lfILexflHrR78++aNDyuZRcuNoacU9SSpUCL3ZnHqva2xkZWXk9A7olvnaajZJfUo362ioMiQzmLa1KQDeIAGYF2FsZMU85BXKsABLWjOxi2FkAYaGBl7VKekdBLl+xDt/vTRBeqo4RonpNoDovor1f8rBjR/7nH53Njvy392kFcV+hDylt13zpnx+f91KvHi3smHrwRCqKi4pYQs8bDvb2fb4x9DQIUB2rJ2qYl1jM/NtOiVOkqAssKbME9TXlikWsvUNYwpkYejiaISmtgEWs0o/jTcwuOZOYCU1THRxsreHoaP/z96csP31RtcjpM4l45bVPsWl/spjiPwAIUTUQXB0s8eCCybh34dx+rzG5EBLU6uoafLd5D7b8eE7W8VUqFFnRYrqqinKMHh7BBUmKsNKKGmoQKCgoRG4xRdVyqgIqeQlcSIA37O2V8Vip+kLt5wUnZs+kZebLWmdO5Vbkz6amZaO+ro7d7NjzbGpEfGIqDh2Lw/c7DuOLb/ciJadK9mlH0D+EqBoAzkxQn7pvJu664ybFsvy90JH/4KHjeP3THahtuPpbWXuhADO3qJJFdia8oJ6O0FKE1dHRAUFqD5SXlZ4vR5NqBXTz/U2lJcUYFh3cr0lbF0KvQ+3nCU+W0T94PKHvq2IugAaHU9vpaWYZHY9Lx49HErHzwDkcOpmK+LQSNDSTWAtBHSiEqOo5tpam+Ptz83D7rbMUGyvYS11tHUuencXz//mWHz11DQlrKsvKB3o7ITBA2sbZ3hF4w6MCUFNTzasCpA6UphK4jPwqpKenY1hUELMi7BSxAsgrDgr0h7erDa/jlZOZJ5uUalmb2WNpiy0NZemZyCjEdKARoqrHWJqpsOSO8fzIr0Rhfy905K+trcXu/cfx1oqdqKoZuGEczZo2NDY0YMyIcO5vSqGnjtWOjw0kKyCnSI4V0BMVUsQbHuQDJycH5RoEfDzhwk4ZtAWAXqfAMBCiqqdQamvmxGg8fv88ODjYQSl6s/x79h7Cvz/airJK6RP3laaCiXqAtwNiokIhFRJAGnQd6O8u2wogj7e4vBZFRcWIHRbGW1qVwNTMFP6+HvBxs8Wh4/Es0hRRpiEgRFVPiY32x9+fv5d3IilZh0oR6uate/C397eyI7/8gnEjFa1qMYe7ix2c7K1hbWHKMuvtMraQ9nQ9HTqRhLvmTJQ0N6GXX6yAQNTV16CARaztEq0AahDILqxGfEISosPVcHF2VM4KYNZGqJ8LswKymR8qIlZ9R4iqnvLCo7dgdOwwRQW1jmWT9x8+jfe+2sPXKcvFwdYMi+dOxIJbxuHuWyfhxuuHY+KoCPh7u8Dezgr5heWSaydp55WTjRGGD4mQ1a7Z29IaGeyDivIKZOSWQ44VUFbVhKycPESF+ikirARZAR4eLnC2t+jxWFtE95M+I0RVD1F1d+HlZxdyv1ApqFj89JkE/OWtDUw45B75uzEszAN/eW4x5t82je9d8vR0h7u7G/z9fPhm1THDw5jH6Yb07CKWYJEm3B0s0p05JZaXWMmhV1iD1V6oqqxAdgFNt5IminQvKGfvT2FhAWLCA3itqGKDrn084GBjgn3HkiESTvqLEFU9xMSoC8sem69IPWrPvNZW7NxzEMte/Rr1TVrIwdioG/feOhYvL7sXQ6LDLzrajyJMG2srRIQFscg1FAeOnUVDU9/LtNqZqIb6O/PMeX/GBlKyKSrMD/V1tSgoqeFZfilQlJ1XUoe0tAyEqD359lmlrICwkABUlxchOasMohFKPxGiqoeYMAF7YOEs2RHbhdTU1GLXj0fx5qdb2ZFfnqCamnTjnlsn4IkH72DHWPc+CQwlj2i1y5mEzD6XFHV0tCOYJZxGDI3o17oRvhiPRflDItTMCijjU6rkFMqXVjfyWQgBfm7w8XJXzApwdrRDQkoWKmuaIdA/SFT7v7NBoFM6uox4O6IS7Np3FK99tBkllfK+nynTtrtvvg7PPn4XXF1d+ywsFLWOGzMck8ZG80qGvtDe0Y2i0mo+FrG/8A0Cnh54bOlcTB8f1ufncCHUApqaU4m/vvEV4pOUa9+lSHxoVDAE+osQVT2DtggUFJbxo7tcNBot9vx4HC++sR41MlcYmxp345kHbsbLv39Ilr9Lj5l30ziofVz79OcpWZWUloeSknIoAQlrSHAAXnpmCeZMHQYLc+m1vmQFZObX4MFnXkdqWibvv+8v1HWldCOHQLcIUdVDPli5FVVV1bKElaLcjVv34sX/robchAjpz9I7J2HpwtlMBOR5u3TUjYwIhaOEOtu6hhZU19ZDKSiy9vH1xtMP3Y5JsUGATCezuqkTf39jJRISU/strDRP1spKmQlZgoFBiKoecja1CBt/OMiz9lKgyf1bdvyItz7bxjw7eZ1SFKHeNn04Hr3vjn5/+E1MTGFm2ndhL6tpwbadh9iNQTm/kSJWtdoPTz98JyaNUMuyAohTycX41ztfIyMrF/2htbWVJdGUu3EIdI9IVOkhlLFOTs2Gs4MFQoP9r9im2jtj8/tt+/DS6+v4OmQ5USpl+X933yzmoS7k05v6i4mJMbbtOtznHVx03E7MKMXBY6cRHeoPJ5bU6U/Sqhe+QcDFCcOig1Bfe74qoFN6VQAtZ9y7/xjGj4mEi5O8OtajJ87ivc8384lUAv1DZP/1GC370MUnZ8HW0gh+51dtXOxDTIJaUlKKTSyyfe/LPXwIhxyMVd14eNEMntyR09l0Mei5bdx+mItYn2GvsYplxpPSsuDpbA0f9tqVElaqSogO80dpaSkfIC7nxtOk7UJWZjZCA714J5cUYaV15B+u2MROIsUQ6CdCVPUcmgh/NikHpSUlMEE7nJ2d+K/TkZaO+o2NTUhMTMI/316NHw4korpO3rHZhB3577xpNF743SJF/T466m7YdoT31kuloroR55KyEKZ2gaeHu2LCSr39wQGeqK6slNUgQNDmgby8fIQH+8DJwQFGxld22VpaNDh46BjeXbkLnaJIVW8hUVX5j1oifoSGAPtpBnpZwsXRFq7O9mhhGf6SinrklDTyGZxysTQDHls8DUsXzVVsmAhBCZ2fTp7BC/9ejcJS6aLai7uTFZ594CbcfOP1ii05pAiaBqi8++lGbD+QgGatvOjey8mMz2gYHTuUv3eXilorq6qwfdchfLh6LxNkUZ+qz3R1di8VkaqhwD6wtU0dKK5sQWZBDfJKGlBd39avlRqWLIn00MKpuPfuOYotw+ulorIKH32xGXFJ+f3qHiI7Iyk9D+hsxfCh8mYD/JreltbocH9UlpcjPVdeg0CjphOnzqXx9S4ujjawtbHm/nfvChSquS1k4v3mxxuwdvMR9vPqfw2uYGChSFW5QZwCg8LSXIUH5l+Pxx+Yr0j31oWQNbF3/3H8eCxFkcV0ZdUtPMpzcbLB3DmzFGnhJeGjDrHH7p/LjuPsk7I3Xl7nVVULvtp4BAdOZkDt5YjJo4Lh7uaMotIq7D3KBLehBRk5pWL9iQEhjv+C32BvbYLfP3ILFtx+k6R10VeCjtVtbW04ffocnv7rclTVK7vzyt7GDI8svB533DINbm6uikTW9JzLysqYFfAdE9Zzspb2CQYP4vgv+A3OdqZ4ZNG0q7LziiLUE6fO4g123M0pVn6jQGtbJ7JyS9DVoUF0ZLCkNdeXgoSZqh2iQn1RzY7xGTklvLtLILgYIvsv+H/YWhpj3o2jsHjBLXx5ntKkpefgfx+vQ0J6OV+udzVo1nQgt7AcJt2tGBoTrlhVAFU9BPi6cQ+0sLRGCKvgoghRFfyMhZkKC+eMwcNL72RHZxcoCR2h8woK8adXP8Hp5FJ0dF1dx4mENSmjEN1tjQgLDYSFAhErJcDoRhMToWaJpypk55XzOQwCwYUIURVwqIzytmkj8dKy+/nWUCWhLHdSSjqe/8sHOJdRqbM5oVpmBSRnFjLPQYPw0ACWbFPGCnBiwjp+dAyKS0uRlV+GLpGREFyAEFUBaIgIDRN56bl74eTkCCWhCDUpOR3/eX8NzqVXMAGSqUD0OBlJp9a2Lu6BmqqUswIIKosaOSQUqq5WpGcVoq1DKKugByGqgxySKdrm+fSDc/jEfiXrUCnLH3c2BX9+7TMksAi1o1N6wayJkQpRwW5Yevt4NDfVo7JWC6m6rGntRAqLWLvbmxAarFakPKx3i8HoEZFMsDtwLikb7aINSgAhqoMe6ucfHxuCxXfeqFz7aXfP6pPTZ5Lw/D+WI7u4QXaEGuznhN8/Ohe33zqLDztJTc1EWbX0gdpkBSSk5aOpoY7dPEJgqVDdLUWsEaFqtGnqcTopH2K3lEBM/h/kWFuZ8hUltra2UIr2jnYcOxGH195bi+JK+S2XVmbdeGThDIweOYyLV6C/H55YeiuLrOW1ojZpOrFm6zF8uWYT72Tqz5DvC6Fyq4XspuRorYy1INB/hKgOYqxZxEZlQkp4jSRSNCDl+E9xePOT9UjJrpSVxCEHwsXBHH9+ZgFmTp8IG5ueiVgWlhYYO2YY3v7bw3CwMZUVE2rbgC82HMbHn3+Dujq5W2N//XxV8PH2xvAIHwgEhBDVQUwHy8x3dHT120slQaXo78jxOLz69hrEZ1TJLpsK8XXCnx6/A3NmTeEDUi58btSMEB0Vjnf/8RBC/Z3k5K5Q39SOFesP4/NVG1HfoJyw+vm6AxC+qkCI6qCmuUWLwtJqdHZ2oj+QqJ44nciy/OuQVSR/ar2PqyV+d//NmDltAqysL+7xUpfU6JFDseyR2xHgKc+2aGjp4P347y//hvu/StDaJtpXBT2IRNUghqbbm5oYYeyIcD6VSdb3YKJ0/MRZ/PX1r5BTUo9umUd+L2dLvPzMYsyYOp7XlF4ueiaP1dvLHcMj/bH74GleOiWV1vYuZGSXsHC9GZFhQXzIt1yam1vw1kfforpBCOtgR2T/Bz0q1Dc2wcvNFmEh6iuuZfk1VNifmJyGf761CukFdZALZfmffuhWTJ00mnunfbEj6LnSUO7YaDUSU7JRLWMrLNWXZmQXo7ujBeGh8sqt+DyDk3FY9f1RdIrW1UGPEFUBH0JCm1nHxUbwbqG+Qkf+xOR0/Pf9tf0q7Pf3sMKLT92NaZOv456pFH+XEmzOTg4IDfJCenomKmo1kArVsabnFrOQuwUjh0VJStr1rqp5e/l3zPaQf1MRGA5CVAWgaLWithmZ2Xm4LjYK1lYWlx303JuU+ulUAl7896dIzq6WV9hvrEKY2hl/WXYvJk8YxWegykmY0eN8mBUwckgQTsadQ21Dq+R0EQlrYloBKivKERMZzMT9ytEyRai5eYVY+c0u7D6SwpcxCgRCVAU/U1hWhzPxaXC0MYWHmzOfo/prYelk4llZWYWd+37CX15fhaLKFtkRqq+HDR5cMJWP6KNSLK22lfmzHcxS6OSC1fNF/91+mf/u+Tcl2uxsbRE7JAQp6VmokLGSpJ1ZATQroKCgCEG+bsxauPg2VLI8aDPt/kMn8dW63Vi/85QQVMHPiB1Vgt/g5WqD2KEhmDsjFu5uLnB1dWZC0s2SMU3IzS9m3uEhxKcUsIiwf6s/qNY0NNCbHbeNYKQy4hEn+aSmZsYwZmJmRHpGovazaNMv/Oq/2e93X/D79DzTswuRXVjJfl2uv9nNfdo7bozFuDHD4OLs/PP6E0pIJSSl4sDxZOw7moQysU9K8CtoSLUQVcFF6IaDrSU7ohvD0twIdLqnYKyNRZJ1DZQQupoJGfmLRX65kPv//GyszFjUbgY/TzteIdHY3Iaqei1qmL2gaW3n9b0Cwa8hURU7qgQXQYW6Ru0lf+9q/93Xwl2+qaWNfxVWSJ81IBjciOJ/gUAgUJD/A3MLiucdDTM+AAAAAElFTkSuQmCC"


@register.simple_tag
def getUserAttending(email, event_id):
    # return datetime.datetime.now().strftime(format_string)
    event = Event.objects.get(id=event_id)
    if User.objects.get(email=email) in event.attending_Students.all():
        return "checked"
    else:
        return ""
@register.simple_tag
def getUserAttendingMeeting(email, meeting_id):
    # return datetime.datetime.now().strftime(format_string)
    meeting = Meeting.objects.get(id=meeting_id)
    if User.objects.get(email=email) in meeting.attending_Members.all():
        return "checked"
    else:
        return ""

def hasClubs(user):
    if hasattr(user, "associated_clubs"):
        if user.associated_clubs.count() > 0:
            return True
        else:
            return False
    else:
        return False
def getVarsities(user):
    varsities = []
    for varsity in Varsity.objects.all():
        if user in varsity.members.all():
            varsities.append(varsity)
    return varsities
def getClubs(user):
    clubs = []
    for club in Club.objects.all():
        if user in club.members.all():
            clubs.append(club)
    return clubs

def Home(request, invalid_login = False):
    home_page = HomePage.objects.first()  # Assuming you have one HomePage instance
    highlights = []
    eventcount = 0
    for event in Event.objects.filter(highlight=True,members_only=False):
        if eventcount >= 2:
            break
        else:
            highlights.append(event)
            eventcount += 1
    newscount = 0
    for news in News.objects.filter(approved=True,awaiting_approval=False):
        if newscount >= 6-eventcount:
            break
        else:
            highlights.append(news)
            newscount += 1
    
    if invalid_login:
        return render(request, "home.html", {'home_page': home_page,"login_failed":"true",'highlights':highlights})
    else:
        return render(request, "home.html", {'home_page': home_page,"login_failed":"false",'highlights':highlights})

def Scouts_View(request):
    
    clubs = Club.objects.all()
    scouts = []
    for club in clubs:
        if "Scouts" in club.about:
            scouts.append(club)
    return render(request, "scouts.html", {'scoutsteams': scouts, 'user': request.user})
def Scouts_Detail(request, scouts_id):
    try:
        scouts = Club.objects.get(id=scouts_id)
        events = Event.objects.filter(author=scouts) 
    except ObjectDoesNotExist:
        return error_404_view(request, None)
    return render(request, "scouts_detail.html", {'scouts': scouts, 'user': request.user, 'events':events, 'links': scouts.links.all()})

def Meetings(request: WSGIRequest):
    meetings = Meeting.objects.all().order_by('-date').order_by('-start_time')
    meetings_filtered = []
    for meeting in meetings:
        print(meeting.attending_Members.all())
        if request.user in meeting.attending_Members.all():
            print(request.user.name)
            meetings_filtered.append(meeting)
    return render(request, "meetings.html", {'hasClubs':hasClubs(request.user),'meetings': meetings_filtered, 'user': request.user})

def Meeting_Details(request, meeting_id):
    try:
        meeting = Meeting.objects.get(id=meeting_id) 
    except ObjectDoesNotExist:
        return error_404_view(request, None) 
    links = meeting.links.all()
    allUsers = User.objects.all()
    return render(request, "meeting_detail.html", {'meeting': meeting, 'links': links, 'allUsers': allUsers, 'user': request.user})

def Events(request):
    events = Event.objects.all().order_by('-published_date')
    return render(request, "events.html", {'hasClubs':hasClubs(request.user),'events': events, 'user': request.user})

def Event_Detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id) 
    except ObjectDoesNotExist:
        return error_404_view(request, None) 
    links = event.links.all()
    allUsers = []
    if event.members_only:
        for member in event.author.members.all():
            if member not in event.attending_Students.all():
                allUsers.append(member)
    else:
        for member in User.objects.all():
            if member not in event.attending_Students.all() and member.associated_student is not None:
                allUsers.append(member) 
    return render(request, "event_detail.html", {'event': event, 'links': links, 'allUsers': allUsers, 'user': request.user})

def News_View(request):
    news = News.objects.all().order_by('-published_date')
    if hasattr(request.user, 'associated_student') and request.user.associated_student is not None:
        grlevel = str(request.user.associated_student.year_level)
        return render(request, "news.html", {'news': news, 'gradelevel': grlevel})
    else:
        return render(request, "news.html", {'news': news})  

def News_Detail(request, news_id):
    try:
        news = News.objects.get(id=news_id)
    except ObjectDoesNotExist:
        return error_404_view(request, None) 
    links = news.links.all()
    return render(request, "news_detail.html", {'news': news, 'links': links})

def Clubs(request):
    tempclubs = Club.objects.all()
    sorted_clubs = sorted(tempclubs, key=lambda club: club.members.count(), reverse=True)
    filtered_clubs = []
    for club in sorted_clubs:
        if "Scouts" not in club.about:
            filtered_clubs.append(club)
    return render(request, "clubs.html", {'clubs': filtered_clubs, 'user': request.user}) 

def Club_Detail(request, club_id):
    club = get_object_or_404(Club, id=club_id) 
    events = Event.objects.filter(author=club) 
    heads = club.heads.all()  
    leadership = club.leadership.all()  
    members = club.members.all()  
    advisors = club.advisors.all()
    links = club.links.all() 

    return render(request, "club_detail.html", {
        'club': club,
        'events': events,
        'heads': heads, 
        'leadership': leadership,
        'members': members, 
        'advisors': advisors,
        'links': links,
        
    })

def Varsity_View(request):
    varsities = Varsity.objects.all()  
    return render(request, "varsity.html", {'varsities': varsities})

def Varsity_Detail(request, varsity_id):
    varsity = get_object_or_404(Varsity, id=varsity_id) 
    captains = varsity.captains.all()
    players = varsity.members.all()  
    coaches = varsity.coaches.all()
    links = varsity.links.all()
    return render(request, "varsity_detail.html", {'varsity': varsity, 'players': players, 'captains': captains, 'coaches': coaches, 'links':links}) 

def Student_Detail(request, student_id):
    user = get_object_or_404(User, id=student_id)
    headclubs = []
    for club in Club.objects.all():
        if user in club.heads.all():
            headclubs.append(club)
    headleadership = []
    for club in Club.objects.all():
        if user in club.leadership.all():
            headleadership.append(club)
    clubs = []
    for club in Club.objects.all():
        if user in club.members.all():
            clubs.append(club)
    varsitiescaptain = []
    for varsity in Varsity.objects.all():
        if user in varsity.captains.all():
            varsitiescaptain.append(varsity)
    varsities = []
    for varsity in Varsity.objects.all():
        if user in varsity.members.all():
            varsities.append(varsity)
    
    return render(request, "student_detail.html", {'selecteduser': user, 'user': request.user, 'headclubs': headclubs, 'headleadership': headleadership, 'clubs': clubs, 'varsitiescaptain': varsitiescaptain, 'varsities':varsities}) 

def Faculty_Detail(request, faculty_id):
    user = get_object_or_404(User, id=faculty_id)
    advisorclubs = []
    for club in Club.objects.all():
        if request.user in club.advisors.all():
            advisorclubs.append(club)
    varsitiescoach = []
    for varsity in Varsity.objects.all():
        if request.user in varsity.coaches.all():
            varsitiescoach.append(varsity)
    return render(request, "faculty_detail.html", {'user': user, 'advisorclubs': advisorclubs, 'varsitiescoach': varsitiescoach}) 

def Club_Varsity_login(request: WSGIRequest):
    user = authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
    if user is not None:
        try:
            print(user.associated_student.color)
            print(user.associated_faculty.color)
            print(user.associated_clubs.color)
            print(user.associated_varsities.color)
        except:
            pass
        if(user.associated_clubs is not None or user.associated_varsities.count() > 0):
            login(request, user)
            return redirect("/")
        else:
            print("user exists but is student or faculty")
            return Home(request, True)
    else:
        print("user does not exist")
        return Home(request, True)

@csrf_exempt
def Student_Faculty_login(request: WSGIRequest):
    if request.method == "GET":
        home_page = HomePage.objects.first()  # Assuming you have one HomePage instance
        return render(request, "home.html", {'home_page': home_page,"login_failed":"false"})
    else:
        body = json.loads(request.body.decode('utf-8'))
        print(body)
        try:
            user = User.objects.get(email=body["username"])
            user.set_password(body["password"])
            user.save()
            authuser = authenticate(username=body["username"],password=body["password"])
            login(request, authuser)
            if request.user.associated_student is None and request.user.associated_faculty is None:
                if "almawakeb" in body["username"]: 
                    string = ""
                    for i in range(10):
                        string += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
                    fac = Faculty.objects.create(faculty_db_id=string)
                    fac.save()
                    user.associated_faculty = fac
                    user.save()
                    return HttpResponse("{\"message\":\"faculty created successfully\"}")
                if "amb" in body["username"]: 
                    return HttpResponse("{\"message\":\"user created successfully complete student setup\"}") 
            return HttpResponse("{\"message\":\"logged in successfully\"}")
        except Exception as e:
            print(e)
            if "amk" in body["username"] or "amg" in body["username"]:
                return HttpResponse("{\"message\":\"only amb allowed on site\"}")
            user = UserManager.create_user(User.objects, body["username"], body["name"], body["password"])
            user.save()
            authuser = authenticate(username=body["username"],password=body["password"])
            login(request, authuser)
            if "almawakeb" in body["username"]: 
                string = ""
                for i in range(10):
                    string += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
                fac = Faculty.objects.create(faculty_db_id=string)
                fac.save()
                user.associated_faculty = fac
                user.save()
                return HttpResponse("{\"message\":\"faculty created successfully\"}")
            if "amb" in body["username"]: 
                return HttpResponse("{\"message\":\"user created successfully complete student setup\"}")
def Student_Faculty_logout(request: WSGIRequest):
    logout(request)
    return redirect("/")
@csrf_exempt
def Finish_Setup_Student(request: WSGIRequest):
    if request.method == "POST":
        try:
            student = Student.objects.get(student_db_id=request.POST.get("student_id"))
        except Exception as e: 
            print(e)
            student = Student.objects.create(student_db_id=request.POST.get("student_id"),year_level=int(request.POST.get("yearlevel")))
        student.year_level=int(request.POST.get("yearlevel"))
        student.section=request.POST.get("sectionletter")
        student.save()
        request.user.associated_student = student
        request.user.save()
        return redirect("/")
    else:
        return HttpResponse("{\"message\":\"ONLY POST ALLOWED\"}")
def UserProfile(request: WSGIRequest):
    if request.user is None:
        return redirect("/")
    else:
        userType = ""
        memberCount = 0
        clubSlashMembers = None
        if request.user.associated_student is not None:
            userType = "student"
            clubSlashMembers = {"clubs":getClubs(request.user),"varsities":getVarsities(request.user)}
        elif request.user.associated_faculty is not None:
            userType = "faculty"
            advisorin = []
            for club in Club.objects.all():
                if request.user in club.advisors.all():
                    advisorin.append(club)
            coachin = []
            for varsity in Varsity.objects.all():
                if request.user in varsity.coaches.all():
                    coachin.append(varsity)
            
            clubSlashMembers = {"clubs": advisorin, "varsities": coachin}
        allUsers = User.objects.all()
        events = []
        for event in Event.objects.all():
            if request.user in event.attending_Students.all():
                events.append(event)
        return render(request, "profile_student.html", {'url':request.build_absolute_uri(), 'user': request.user, 'userType': userType,"clubSlashMembers": clubSlashMembers, 'allUsers': allUsers, 'attendingEvents':events, 'litAllUsers': User.objects.all()})

def ClubProfile(request: WSGIRequest, club_id):
    if request.user is None:
        return redirect("/")
    else:
        memberCount = 0
        clubSlashMembers = None
        allUsers = User.objects.all()
        events = []
        for event in Event.objects.all():
            if request.user in event.attending_Students.all():
                events.append(event) 
        club = Club.objects.get(id=club_id)
        if club in request.user.associated_clubs.all():
            return render(request, "profile_club.html", {'url':request.build_absolute_uri(), 'user': request.user, 'club': club,"clubSlashMembers": clubSlashMembers, 'allUsers': allUsers, 'attendingEvents':events})
        else:
            return HttpResponse("<h1>YOU DO NOT HAVE PERMISSION TO THIS CLUB</h1>")
def VarsityProfile(request: WSGIRequest, varsity_id: int):
    if request.user is None:
        return redirect("/")
    else:
        userType = ""
        memberCount = 0
        clubSlashMembers = None
        allUsers = User.objects.all()
        events = []
        for event in Event.objects.all():
            if request.user in event.attending_Students.all():
                events.append(event)
        varsity: Varsity = Varsity.objects.get(id=varsity_id)
        if varsity not in request.user.associated_varsities.all():
            return HttpResponse("<h1>YOU ARE NOT A CLUB, OPERATION FAILED</h1>")
        return render(request, "profile_varsity.html", {'varsity': varsity, 'url':request.build_absolute_uri(), 'user': request.user,"clubSlashMembers": clubSlashMembers, 'allUsers': allUsers, 'attendingEvents':events})

def CreateEvent(request:WSGIRequest, club_id):
    if request.user.associated_clubs is None:
        return HttpResponse("<h1>CLUB ENDPOINT ONLY</h1>")
    club = Club.objects.get(id=club_id)
    if request.method == "GET":
        students = []
        for user in User.objects.all():
            if user.associated_student is not None:
                students.append(user)
        faculty = []
        for user in User.objects.all():
            if user.associated_faculty is not None:
                faculty.append(user)
        return render(request, "create_event.html", {'user': request.user, 'members': students,  'faculties': faculty, 'club':club}) 
    elif request.method == "POST":
        file = request.FILES.get("coverPhoto")
        if file is not None:
            filename = os.path.join(settings.MEDIA_ROOT,"event_covers", str(random.randint(11111111,999999999)) + file.name)
            with open(filename, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            event = Event.objects.create(author=club, significant_event=(request.POST.get("significant") is not None), cover=filename.replace(str(settings.BASE_DIR), '').replace("/media",""), title=request.POST.get("title"), text=request.POST.get("content"), summary=request.POST.get("summary"), date=request.POST.get("date"), start_time=request.POST.get("starttime"), end_time=request.POST.get("endtime"), location=request.POST.get("location"), color=club, members_only=(request.POST.get("membersonly") is not None), highlight=(request.POST.get("highlight") is not None), group=request.POST.get("gradefilter"), grade=request.POST.get("sectionfilter"), published_date=datetime.datetime.now())
        else: 
            event = Event.objects.create(author=club, significant_event=(request.POST.get("significant") is not None), title=request.POST.get("title"), text=request.POST.get("content"), summary=request.POST.get("summary"), date=request.POST.get("date"), start_time=request.POST.get("starttime"), end_time=request.POST.get("endtime"), location=request.POST.get("location"), color=club, members_only=(request.POST.get("membersonly") is not None), highlight=(request.POST.get("highlight") is not None), group=request.POST.get("gradefilter"), grade=request.POST.get("sectionfilter"), published_date=datetime.datetime.now())
        linkstr = request.POST.get("links")
        print("(" + linkstr + ")")
        if linkstr is not None and linkstr != "":
            for link in linkstr.split("\n"):
                linkobj = Links.objects.create(name=link[:link.find("!")], link=link[link.find("!")+1:])
                event.links.add(linkobj)
        listofemails = []
        for member in User.objects.all():
            if request.POST.get(member.email) is not None:
                event.attending_Students.add(member) 
                listofemails.append(member.email) 
        if request.POST.get("emailstudent") is not None:
            print("emailing students")
            if len(listofemails) > 0:
                email = ""
                with open(os.path.join(settings.BASE_DIR, "templates", "students_email.html"), 'r') as f: 
                    email = f.read()
                    email = email.replace("{{title}}",event.title)
                    email = email.replace("{{summary}}",event.summary)
                    email = email.replace("{{author}}",event.author.name)
                    email = email.replace("{{event_id}}",str(event.pk)) 
                    email = email.replace("{{logo}}",logo) 
                    email = email.replace("{{email}}",request.user.email) 
                    email = email.replace("{{text}}",event.text) 
                    email = email.replace("{{date}}",event.date) 
                    email = email.replace("{{start_time}}",event.start_time) 
                    email = email.replace("{{end_time}}",event.end_time) 
                send_mail("New Event", "Students' Society", None, listofemails, False, html_message=email)

        if request.POST.get("emailhos") is not None:
            print("emailing hos")
            hosemails = []
            for member in User.objects.all():
                if request.POST.get(member.email) is not None:
                    hosemails.append(member.email)
            if len(hosemails) > 0: 
                email = ""
                with open(os.path.join(settings.BASE_DIR, "templates", "hos_email.html"), 'r') as f:
                    email = f.read()
                    email = email.replace("{{title}}",event.title)
                    email = email.replace("{{summary}}",event.summary)
                    email = email.replace("{{author}}",event.author.name)
                    email = email.replace("{{event_id}}",str(event.pk)) 
                    email = email.replace("{{logo}}",logo) 
                    email = email.replace("{{email}}",request.user.email) 
                    email = email.replace("{{text}}",event.text) 

                    email = email.replace("{{date}}",event.date) 
                    email = email.replace("{{start_time}}",event.start_time) 
                    email = email.replace("{{end_time}}",event.end_time) 
                send_mail("New Event", "Students' Society", None, hosemails, False, html_message=email)
        event.save()
        return redirect("/Event/Detail/" + str(event.pk)) 
def ModifyEvent(request: WSGIRequest, event_id):
    event = Event.objects.get(id=event_id)
    if event.author not in request.user.associated_clubs.all():
        return HttpResponse("<h1>YOU ARE NOT THE AUTHOR OF THIS EVENT, OPERATION FAILED</h1>")
    students = []
    for user in User.objects.all():
        if user.associated_student is not None:
            students.append(user)
    faculty = []
    for user in User.objects.all():
        if user.associated_faculty is not None:
            faculty.append(user)
    links = ""
    for link in event.links.all():
        links += link.name + "!" + link.link + "\n"
    links = links[:-1]
    membersonly = ""
    if event.members_only:
        membersonly = "checked"
    else:
        membersonly = ""
    if request.method == "GET":
        return render(request, "modify_event.html", {'event':event, 'allUsers': students, 'faculties': faculty, 'links': links, 'membersonly': membersonly})
    elif request.method == "POST":
        event.title = request.POST.get("title")
        event.text = request.POST.get("content")
        event.summary = request.POST.get("summary")
        event.date = request.POST.get("date")
        event.location = request.POST.get("location")
        event.group = request.POST.get("gradefilter")
        event.grade = request.POST.get("sectionfilter")
        event.start_time=request.POST.get("starttime")
        event.end_time=request.POST.get("endtime")  
        event.published_date = datetime.datetime.now()
        event.members_only = request.POST.get("membersonly") is not None
        event.highlight = request.POST.get("highlight") is not None
        file = request.FILES.get("coverPhoto")
        if file is not None:
            filename = os.path.join(settings.MEDIA_ROOT,"event_covers", str(random.randint(11111111,999999999)) + file.name)
            with open(filename, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            event.cover = filename.replace(str(settings.BASE_DIR), '').replace("/media","")
        linkstr = request.POST.get("links")
        print("(" + linkstr + ")")
        event.links.clear() 
        if linkstr is not None and linkstr != "":
            for link in linkstr.split("\n"):
                linkobj = Links.objects.create(name=link[:link.find("!")], link=link[link.find("!")+1:])
                event.links.add(linkobj)
        listofemails = []
        for member in User.objects.all():
            if request.POST.get(member.email) is not None:
                event.attending_Students.add(member)
                print("student")
                print(member)
                listofemails.append(str(member.email))
            else:
                event.attending_Students.remove(member)
                try:
                    listofemails.remove(str(member.email))
                except:
                    pass 
        print(listofemails)
        if request.POST.get("emailstudent") is not None:
            print("emailing students")
            if len(listofemails) > -1:
                email = ""
                with open(os.path.join(settings.BASE_DIR, "templates", "students_email.html"), 'r') as f:
                    email = f.read()
                    email = email.replace("{{title}}",event.title)
                    email = email.replace("{{summary}}",event.summary)
                    email = email.replace("{{author}}",event.author.name)
                    email = email.replace("{{event_id}}",str(event.pk)) 
                    email = email.replace("{{logo}}",logo) 
                    email = email.replace("{{email}}",request.user.email) 
                    email = email.replace("{{text}}",event.text) 

                    email = email.replace("{{date}}",event.date) 
                    email = email.replace("{{start_time}}",event.start_time) 
                    email = email.replace("{{end_time}}",event.end_time) 
                send_mail("Event Details Changed", "Students' Society", None, listofemails, False, html_message=email)

        if request.POST.get("emailhos") is not None:
            print("emailing hos")
            hosemails = []
            for member in User.objects.all():
                if request.POST.get(member.email) is not None:
                    hosemails.append(member.email)
            if len(hosemails) > 0: 
                email = ""
                with open(os.path.join(settings.BASE_DIR, "templates", "hos_email.html"), 'r') as f:
                    email = f.read()
                    email = email.replace("{{title}}",event.title)
                    email = email.replace("{{summary}}",event.summary)
                    email = email.replace("{{author}}",event.author.name)
                    email = email.replace("{{event_id}}",str(event.pk)) 
                    email = email.replace("{{logo}}",logo) 
                    email = email.replace("{{email}}",request.user.email) 
                    email = email.replace("{{text}}",event.text) 

                    email = email.replace("{{date}}",event.date) 
                    email = email.replace("{{start_time}}",event.start_time) 
                    email = email.replace("{{end_time}}",event.end_time) 
                send_mail("Event Details Changed", "Students' Society", None, hosemails, False, html_message=email)
        event.save()
        return redirect("/Event/Detail/" + str(event.pk))
def CreateMeeting(request:WSGIRequest, club_id):
    club = Club.objects.get(id=club_id)
    if request.method == "GET":
        students = []
        for user in User.objects.all():
            students.append(user) 
        allusers = []
        for member in club.members.all():
            allusers.append(member)
        for head in club.heads.all():
            allusers.append(head)
        for leadership in club.leadership.all():
            allusers.append(leadership)
        
        return render(request, "create_meeting.html", {'user': request.user, 'members': students, 'club':club, 'allUsers': allusers}) 
    elif request.method == "POST":
        meeting = Meeting.objects.create(author=club, title=request.POST.get("title"), text=request.POST.get("content"), date=request.POST.get("date"), start_time=request.POST.get("starttime"), end_time=request.POST.get("endtime"), location=request.POST.get("location"), published_date=datetime.datetime.now())
        linkstr = request.POST.get("links")
        print("(" + linkstr + ")")
        if linkstr is not None and linkstr != "":
            for link in linkstr.split("\n"):
                linkobj = Links.objects.create(name=link[:link.find("!")], link=link[link.find("!")+1:])
                meeting.links.add(linkobj)
        listofemails = []
        for member in User.objects.all():
            if request.POST.get(member.email) is not None:
                meeting.attending_Members.add(member) 
                listofemails.append(member.email) 
        if request.POST.get("emailstudent") is not None:
            print("emailing students")
            if len(listofemails) > 0:
                email = ""
                with open(os.path.join(settings.BASE_DIR, "templates", "meeting_email.html"), 'r') as f: 
                    email = f.read()
                    email = email.replace("{{title}}",meeting.title)
                    email = email.replace("{{author}}",meeting.author.name)
                    email = email.replace("{{event_id}}",str(meeting.pk)) 
                    email = email.replace("{{logo}}",logo)
                    email = email.replace("{{text}}",meeting.text) 
                    email = email.replace("{{date}}",meeting.date) 
                    email = email.replace("{{start_time}}",meeting.start_time) 
                    email = email.replace("{{end_time}}",meeting.end_time) 
                send_mail("New Meeting", "Students' Society", None, listofemails, False, html_message=email)

        if request.POST.get("emailhos") is not None:
            print("emailing hos")
            hosemails = []
            for member in User.objects.all():
                if request.POST.get(member.email) is not None:
                    hosemails.append(member.email)
            if len(hosemails) > 0: 
                email = ""
                with open(os.path.join(settings.BASE_DIR, "templates", "meeting_email.html"), 'r') as f:
                    email = f.read()
                    email = email.replace("{{title}}",meeting.title)
                    email = email.replace("{{summary}}",meeting.summary)
                    email = email.replace("{{author}}",meeting.author.name)
                    email = email.replace("{{event_id}}",str(meeting.pk)) 
                    email = email.replace("{{logo}}",logo) 
                    email = email.replace("{{email}}",request.user.email) 
                    email = email.replace("{{text}}",meeting.text) 

                    email = email.replace("{{date}}",meeting.date) 
                    email = email.replace("{{start_time}}",meeting.start_time) 
                    email = email.replace("{{end_time}}",meeting.end_time) 
                send_mail("New Meeting", "Students' Society", None, hosemails, False, html_message=email)
        meeting.save()
        return redirect("/Meetings/Detail/" + str(meeting.pk)) 
def ModifyMeeting(request: WSGIRequest, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    if meeting.author not in request.user.associated_clubs.all():
        return HttpResponse("<h1>YOU ARE NOT THE AUTHOR OF THIS EVENT, OPERATION FAILED</h1>")
    students = []
    for user in User.objects.all():
        students.append(user)
    links = ""
    for link in meeting.links.all():
        links += link.name + "!" + link.link + "\n"
    links = links[:-1]
    if request.method == "GET":
        return render(request, "modify_meeting.html", {'meeting':meeting, 'allUsers': students, 'links': links})
    elif request.method == "POST":
        meeting.title = request.POST.get("title")
        meeting.text = request.POST.get("content")
        meeting.date = request.POST.get("date")
        meeting.location = request.POST.get("location")
        meeting.start_time=request.POST.get("starttime")
        meeting.end_time=request.POST.get("endtime")
        meeting.published_date = datetime.datetime.now()
        linkstr = request.POST.get("links")
        print("(" + linkstr + ")")
        meeting.links.clear()
        if linkstr is not None and linkstr != "":
            for link in linkstr.split("\n"):
                linkobj = Links.objects.create(name=link[:link.find("!")], link=link[link.find("!")+1:])
                meeting.links.add(linkobj)
        listofemails = []
        for member in User.objects.all():
            if request.POST.get(member.email) is not None:
                meeting.attending_Members.add(member)
                print("student")
                print(member)
                listofemails.append(str(member.email))
            else:
                meeting.attending_Members.remove(member)
                try:
                    listofemails.remove(str(member.email))
                except:
                    pass 
        print(listofemails)
        if request.POST.get("emailstudent") is not None:
            print("emailing students")
            if len(listofemails) > -1:
                email = ""
                with open(os.path.join(settings.BASE_DIR, "templates", "meeting_email.html"), 'r') as f:
                    email = f.read()
                    email = email.replace("{{title}}",meeting.title)
                    email = email.replace("{{author}}",meeting.author.name)
                    email = email.replace("{{event_id}}",str(meeting.pk)) 
                    email = email.replace("{{logo}}",logo) 
                    email = email.replace("{{email}}",request.user.email) 
                    email = email.replace("{{text}}",meeting.text) 

                    email = email.replace("{{date}}",meeting.date) 
                    email = email.replace("{{start_time}}",meeting.start_time) 
                    email = email.replace("{{end_time}}",meeting.end_time) 
                send_mail("Meeting Details Changed", "Students' Society", None, listofemails, False, html_message=email)

        if request.POST.get("emailhos") is not None:
            print("emailing hos")
            hosemails = []
            for member in User.objects.all():
                if request.POST.get(member.email) is not None:
                    hosemails.append(member.email)
            if len(hosemails) > 0: 
                email = ""
                with open(os.path.join(settings.BASE_DIR, "templates", "meeting_email.html"), 'r') as f:
                    email = f.read()
                    email = email.replace("{{title}}",meeting.title)
                    email = email.replace("{{author}}",meeting.author.name)
                    email = email.replace("{{event_id}}",str(meeting.pk)) 
                    email = email.replace("{{logo}}",logo) 
                    email = email.replace("{{email}}",request.user.email) 
                    email = email.replace("{{text}}",meeting.text) 

                    email = email.replace("{{date}}",meeting.date) 
                    email = email.replace("{{start_time}}",meeting.start_time) 
                    email = email.replace("{{end_time}}",meeting.end_time) 
                send_mail("Meeting Details Changed", "Students' Society", None, hosemails, False, html_message=email)
        meeting.save()
        return redirect("/Meetings/Detail/" + str(meeting.pk))

def CreateNews(request: WSGIRequest):
    if request.method == "GET":
        return render(request, "create_news.html", {'user': request.user})
    elif request.method == "POST":
        file = request.FILES.get("coverPhoto")
        if file is not None:
            filename = os.path.join(settings.MEDIA_ROOT,"news_covers", str(random.randint(11111111,999999999)) + file.name)
            with open(filename, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            event = News.objects.create(author=request.user, cover=filename.replace(str(settings.BASE_DIR), '').replace("/media",""), title=request.POST.get("title"), text=request.POST.get("content"), published_date=datetime.datetime.now(), summary=request.POST.get("summary"), highlight=(request.POST.get("highlight") is not None), group=request.POST.get("gradefilter"), grade=request.POST.get("sectionfilter"))  
        else: 
            event = News.objects.create(author=request.user, title=request.POST.get("title"), text=request.POST.get("content"), published_date=datetime.datetime.now(), summary=request.POST.get("summary"), highlight=(request.POST.get("highlight") is not None), group=request.POST.get("gradefilter"), grade=request.POST.get("sectionfilter"))  
        linkstr = request.POST.get("links")
        print("(" + linkstr + ")")
        if linkstr is not None and linkstr != "": 
            for link in linkstr.split("\n"):
                linkobj = Links.objects.create(name=link[:link.find("!")], link=link[link.find("!")+1:]) 
                event.links.add(linkobj)
        event.save()
        email = ""
        with open(os.path.join(settings.BASE_DIR, "templates", "new_news_email.html"), 'r') as f:
            email = f.read()
            email = email.replace("{{title}}",event.title)
            email = email.replace("{{summary}}",event.summary)
            email = email.replace("{{author}}",event.author.name)
            email = email.replace("{{event_id}}",str(event.pk)) 
            email = email.replace("{{logo}}",logo) 
            email = email.replace("{{email}}",request.user.email) 
            email = email.replace("{{text}}",event.text) 
        officers = ['mohamad.moukayed@amb.sch.ae', 'sulaiman.abuqamar@amb.sch.ae']
        for user in User.objects.all():
            if user.is_admin:
                officers.append(str(user.email))
        send_mail("News Post Awaiting Approval", "Students' Society", None, officers, False, html_message=email)
        return redirect("/News/Detail/" + str(event.pk)) 

def ModifyNews(request: WSGIRequest, news_id):
    news = News.objects.get(id=news_id)
    if request.user != news.author:
        return HttpResponse("<h1>YOU ARE NOT THE AUTHOR OF THIS NEWS POST, OPERATION FAILED</h1>")
    students = []
    for user in User.objects.all():
        if user.associated_student is not None:
            students.append(user)
    faculty = []
    for user in User.objects.all():
        if user.associated_faculty is not None:
            faculty.append(user)
    links = ""
    for link in news.links.all():
        links += link.name + "!" + link.link + "\n"
    links = links[:-1]
    if request.method == "GET":
        print(news.grade)
        print(news.group)
        return render(request, "modify_news.html", {'news':news, 'allUsers': students, 'faculties': faculty, 'links': links})
    elif request.method == "POST":
        news.title = request.POST.get("title")
        news.text = request.POST.get("content")
        news.summary = request.POST.get("summary")
        news.group = request.POST.get("gradefilter")
        news.grade = request.POST.get("sectionfilter")
        news.published_date = datetime.datetime.now()
        news.highlight = request.POST.get("highlight") is not None
        news.approved = False
        news.awaiting_approval = True
        file = request.FILES.get("coverPhoto")
        if file is not None:
            filename = os.path.join(settings.MEDIA_ROOT,"event_covers", str(random.randint(11111111,999999999)) + file.name)
            with open(filename, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            news.cover = filename.replace(str(settings.BASE_DIR), '').replace("/media","")
        linkstr = request.POST.get("links")
        print("(" + linkstr + ")")
        news.links.clear()
        if linkstr is not None and linkstr != "":
            for link in linkstr.split("\n"):
                linkobj = Links.objects.create(name=link[:link.find("!")], link=link[link.find("!")+1:])
                news.links.add(linkobj)
        email = ""
        with open(os.path.join(settings.BASE_DIR, "templates", "new_news_email.html"), 'r') as f:
            email = f.read()
            email = email.replace("{{title}}",news.title)
            email = email.replace("{{summary}}",news.summary)
            email = email.replace("{{author}}",news.author.name)
            email = email.replace("{{event_id}}",str(news.pk)) 
            email = email.replace("{{logo}}",logo) 
            email = email.replace("{{email}}",request.user.email) 
            email = email.replace("{{text}}",news.text) 
        officers = ['mohamad.moukayed@amb.sch.ae', 'sulaiman.abuqamar@amb.sch.ae']
        for user in User.objects.all():
            if user.is_admin:
                officers.append(str(user.email))
        send_mail("News Post Awaiting Approval", "Students' Society", None, officers, False, html_message=email)
        news.save()
        return redirect("/News/Detail/" + str(news.pk))

def MeetingAttendeePermissionSlips(request: WSGIRequest, meeting_id: int):
    meeting = Meeting.objects.get(id=meeting_id)
    return render(request, "permission_slips.html", {'attendees': meeting.attending_Members.all(), 'meeting': meeting})

def AttendeesListPrintable(request: WSGIRequest, event_id: int):
    event = Event.objects.get(id=event_id)
    return render(request, "printable_attendees_list.html", {'attendees': event.attending_Students.all(), 'event': event})

def removeAttendee(request: WSGIRequest):
    event = Event.objects.get(id=int(request.GET.get("id")))
    if event.author not in request.user.associated_clubs.all() and request.GET.get("email") != request.user.email:
        return HttpResponse("<h1>YOU ARE NOT THE AUTHOR OF THIS EVENT, OPERATION FAILED</h1>")
    event.attending_Students.remove(User.objects.get(email=request.GET.get("email")))
    try:
        event.confirmed_Students.remove(User.objects.get(email=request.GET.get("email")))
    except:
        pass
    return HttpResponse("{\"message\":\"competed\"}")
def addAttendeeMeeting(request: WSGIRequest):
    meeting = Meeting.objects.get(id=int(request.GET.get("id")))
    if meeting.author not in request.user.associated_clubs.all() and request.GET.get("email") != request.user.email:
        return HttpResponse("<h1>YOU ARE NOT THE AUTHOR OF THIS EVENT, OPERATION FAILED</h1>")
    meeting.attending_Members.add(User.objects.get(email=request.GET.get("email")))
    return HttpResponse("{\"message\":\"competed\"}")
def removeAttendeeMeeting(request: WSGIRequest):
    meeting = Meeting.objects.get(id=int(request.GET.get("id")))
    if meeting.author not in request.user.associated_clubs.all() and request.GET.get("email") != request.user.email:
        return HttpResponse("<h1>YOU ARE NOT THE AUTHOR OF THIS EVENT, OPERATION FAILED</h1>")
    meeting.attending_Members.remove(User.objects.get(email=request.GET.get("email")))
    try:
        meeting.attending_Members.remove(User.objects.get(email=request.GET.get("email")))
    except:
        pass
    return HttpResponse("{\"message\":\"competed\"}")
def addAttendee(request: WSGIRequest):
    event = Event.objects.get(id=int(request.GET.get("id")))
    if event.author not in request.user.associated_clubs.all() and request.GET.get("email") != request.user.email:
        return HttpResponse("<h1>YOU ARE NOT THE AUTHOR OF THIS EVENT, OPERATION FAILED</h1>")
    event.attending_Students.add(User.objects.get(email=request.GET.get("email")))
    return HttpResponse("{\"message\":\"competed\"}")

def setConfirmed(request: WSGIRequest):
    event = Event.objects.get(id=int(request.GET.get("id")))
    user = User.objects.get(email=request.GET.get("email"))
    if user != request.user and event.author not in request.user.associated_clubs.all(): 
        return HttpResponse("<h1>YOU ARE NOT THE LOGGED IN USER, OPERATION FAILED</h1>")
    event.confirmed_Students.add(user)
    return HttpResponse("{\"message\":\"competed\"}")
def setUnconfirmed(request: WSGIRequest):
    event = Event.objects.get(id=int(request.GET.get("id")))
    user = User.objects.get(email=request.GET.get("email"))
    if user != request.user and event.author not in request.user.associated_clubs.all():
        return HttpResponse("<h1>YOU ARE NOT THE LOGGED IN USER, OPERATION FAILED</h1>")
    event.confirmed_Students.remove(user)
    return HttpResponse("{\"message\":\"competed\"}")

def removeClubMember(request: WSGIRequest, club_id: int, sector: str):
    club: Club = Club.objects.get(id=club_id)
    if club not in request.user.associated_clubs.all():
        return HttpResponse("<h1>YOU ARE NOT A CLUB, OPERATION FAILED</h1>")
    if sector == "Member":
        club.members.remove(User.objects.get(email=request.GET.get("email")))
    elif sector == "Head":
        club.heads.remove(User.objects.get(email=request.GET.get("email")))
    elif sector == "Advisor":
        club.advisors.remove(User.objects.get(email=request.GET.get("email")))
    elif sector == "Leadership":
        club.leadership.remove(User.objects.get(email=request.GET.get("email")))
    else:
        return HttpResponse("{\"message\":\"invalid sector\"}")
    return HttpResponse("{\"message\":\"competed\"}")
def addClubMember(request: WSGIRequest, club_id: int, sector: str):
    club: Club = Club.objects.get(id=club_id)
    if club not in request.user.associated_clubs.all():
        return HttpResponse("<h1>YOU ARE NOT A CLUB, OPERATION FAILED</h1>")
    if sector == "Member":
        club.members.add(User.objects.get(email=request.GET.get("email")))
    elif sector == "Head":
        club.heads.add(User.objects.get(email=request.GET.get("email")))
    elif sector == "Advisor":
        club.advisors.add(User.objects.get(email=request.GET.get("email")))
    elif sector == "Leadership":
        club.leadership.add(User.objects.get(email=request.GET.get("email")))
    
    return HttpResponse("{\"message\":\"competed\"}")

def removeVarsityPlayer(request: WSGIRequest, varsity_id: int,  sector: str):
    varsity: Varsity = Varsity.objects.get(id=varsity_id)
    if varsity not in request.user.associated_varsities.all():
        return HttpResponse("<h1>YOU ARE NOT A VARSITY, OPERATION FAILED</h1>")
    if sector == "Member":
        varsity.members.remove(User.objects.get(email=request.GET.get("email")))
    elif sector == "Captain":
        varsity.captains.remove(User.objects.get(email=request.GET.get("email")))
    elif sector == "Coach":
        varsity.coaches.remove(User.objects.get(email=request.GET.get("email")))
    varsity.save() 
    return HttpResponse("{\"message\":\"competed\"}")
def addVarsityPlayer(request: WSGIRequest, varsity_id: int, sector: str):
    varsity: Varsity = Varsity.objects.get(id=varsity_id)
    if varsity not in request.user.associated_varsities.all():
        return HttpResponse("<h1>YOU ARE NOT A VARSITY, OPERATION FAILED</h1>")
    if sector == "Member":
        varsity.members.add(User.objects.get(email=request.GET.get("email")))
    elif sector == "Captain":
        varsity.captains.add(User.objects.get(email=request.GET.get("email")))
    elif sector == "Coach":
        varsity.coaches.add(User.objects.get(email=request.GET.get("email")))
    varsity.save()
    return HttpResponse("{\"message\":\"competed\"}")

def editProfile(request:WSGIRequest):
    if request.method == "GET":
        return render(request, "edit_profile.html", {'userType': 'student' if request.user.associated_student is not None else 'faculty', 'user': request.user})
    elif request.method == "POST":
        userType = "student" if request.user.associated_student is not None else "faculty"
        if userType == "student":
            file = request.FILES.get("coverPhoto")
            if file is not None:
                filename = os.path.join(settings.MEDIA_ROOT,"profiles", str(random.randint(11111111,999999999)) + file.name)
                with open(filename, 'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                request.user.associated_student.profile_picture = filename.replace(str(settings.BASE_DIR), '').replace("/media","")
            request.user.associated_student.about = request.POST.get("content")
            request.user.associated_student.save()
            request.user.save()
        elif userType == "faculty":
            file = request.FILES.get("coverPhoto")
            if file is not None:
                filename = os.path.join(settings.MEDIA_ROOT,"profiles", str(random.randint(11111111,999999999)) + file.name)
                with open(filename, 'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                request.user.associated_faculty.profile_picture = filename.replace(str(settings.BASE_DIR), '').replace("/media","")
            request.user.associated_faculty.save()
            request.user.save()
        return redirect("/profile/User") 
def editVarsity(request:WSGIRequest, varsity_id: int):
    varsity: Varsity = Varsity.objects.get(id=varsity_id)
    if varsity not in request.user.associated_varsities.all():
        return HttpResponse("<h1>YOU ARE NOT A VARSITY, OPERATION FAILED</h1>")
    if request.method == "GET":
        links = ""
        for link in varsity.links.all():
            links += link.name + "!" + link.link + "\n"
        links = links[:-1]
        return render(request, "edit_profile.html", { 'userType':'varsity', 'varsity':varsity, 'user': request.user, 'links': links})
    elif request.method == "POST":
        
        varsity.name = request.POST.get("name")
        varsity.about = request.POST.get("about")
        varsity.color = request.POST.get("color")
        varsity.about = request.POST.get("content")
        linkstr = request.POST.get("links")
        print("(" + linkstr + ")")
        varsity.links.clear()
        if linkstr is not None and linkstr != "":
            for link in linkstr.split("\n"):
                linkobj = Links.objects.create(name=link[:link.find("!")], link=link[link.find("!")+1:])
                varsity.links.add(linkobj)
        file = request.FILES.get("coverPhoto")
        if file is not None:
            filename = os.path.join(settings.MEDIA_ROOT,"clubs_logos", str(random.randint(11111111,999999999)) + file.name) 
            with open(filename, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            varsity.logo = filename.replace(str(settings.BASE_DIR), '').replace("/media","")
        varsity.save() 
        request.user.save() 
        return redirect("/profile/Varsity/" + str(varsity.pk))
def editClub(request:WSGIRequest, club_id: int):
    club: Club = Club.objects.get(id=club_id)
    if club not in request.user.associated_clubs.all():
        return HttpResponse("<h1>YOU ARE NOT A CLUB, OPERATION FAILED</h1>")
    if request.method == "GET":
        links = ""
        for link in club.links.all():
            links += link.name + "!" + link.link + "\n"
        links = links[:-1]
        return render(request, "edit_profile.html", {'userType':'club','club':club, 'user': request.user, 'links': links}) 
    elif request.method == "POST":
        club.name = request.POST.get("name")
        club.about = request.POST.get("about")
        club.color = request.POST.get("color")
        club.about = request.POST.get("content")
        linkstr = request.POST.get("links")
        print("(" + linkstr + ")")
        club.links.clear()
        if linkstr is not None and linkstr != "":
            for link in linkstr.split("\n"):
                linkobj = Links.objects.create(name=link[:link.find("!")], link=link[link.find("!")+1:])
                club.links.add(linkobj)
        file = request.FILES.get("coverPhoto")
        if file is not None:
            filename = os.path.join(settings.MEDIA_ROOT,"clubs_logos", str(random.randint(11111111,999999999)) + file.name)
            with open(filename, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            club.logo = filename.replace(str(settings.BASE_DIR), '').replace("/media","")
        club.save()  
        request.user.save()
        return redirect("/profile/Club/" + str(club.pk))

def clubSendEmails(request: WSGIRequest, club_id):
    club: Club = Club.objects.get(id=club_id)
    listofaccepted = []
    listofrejected = []
    listofemails = []
    for user in User.objects.all():
        if request.POST.get(user.email) is not None:
            listofemails.append(user) 
    for user in listofemails: 
        if user in club.members.all(): 
            listofaccepted.append(str(user.email)) 
        else:
            listofrejected.append(str(user.email))
    listofheads = []
    for head in club.heads.all():
        listofheads.append(str(head.email))
    email = ""
    with open(os.path.join(settings.BASE_DIR, "templates", "acceptance_letter.html"), 'r') as f: 
        email = f.read()
        email = email.replace("{{name}}",club.name)
        email = email.replace("{{title}}",club.name)
        email = email.replace("{{club_id}}",str(club.pk)) 
        email = email.replace("{{addon}}",request.POST.get("content")) 
        email = email.replace("{{logo}}",logo) 
        email = email.replace("{{email}}",request.user.email)
    msg = EmailMessage(subject=club.name + " Admission", body=email, from_email=None, to=listofaccepted,cc=listofheads)
    msg.content_subtype = "html"
    msg.send()

    email = ""
    with open(os.path.join(settings.BASE_DIR, "templates", "rejection_letter.html"), 'r') as f: 
        email = f.read()
        email = email.replace("{{name}}",club.name)
        email = email.replace("{{title}}",club.name)
        email = email.replace("{{club_id}}",str(club.pk)) 
        email = email.replace("{{logo}}",logo) 
        email = email.replace("{{email}}",request.user.email)
    msg = EmailMessage(subject=club.name + " Admission", body=email, from_email=None, to=listofrejected,cc=listofheads)
    msg.content_subtype = "html"
    msg.send() 
    
    # send_mail("New Event", "Students' Society", None, ["mohamad.moukayed@amb.sch.ae"], False, html_message=email)
    return redirect("/profile/Club/" + str(club.pk))

def error_404_view(request, exception):
   
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html', status=404) 
def error_500_view(request):
   
    # we add the path to the 500.html file
    # here. The name of our HTML file is 404.html
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return render(request, '500.html', {'exc': exc_value, 'exc_trace': exc_traceback}, status=500) 

def restartServer():
    time.sleep(2)
    os.execv(sys.executable, ['python'] + sys.argv)
def ActivateSystemUpdate(request: WSGIRequest):
    if request.user.is_superuser and request.user.is_admin:
        
        os.system("git pull origin prod")
        print("restarting Server")
        Thread(target=restartServer).start() 
        return HttpResponse("{\"message\":\"System Updated Successfully, Rebooting...\"}",status=200)
    else:
        return HttpResponse("Not Authorized",status=401)
def PrepareSystemUpdate(request: WSGIRequest):
    if request.user.is_superuser and request.user.is_admin:
        print("adding changes")
        os.system("git add *")
        print("commit")
        os.system("git commit -m \"Current Data\"")
        print("pushing")
        os.system("git push origin data")
        return HttpResponse("{\"message\":\"Current Server Pushed\"}",status=200)
    else:
        return HttpResponse("Not Authorized",status=401)
    
@csrf_exempt
def uploadImage(request:WSGIRequest):
    file = request.FILES.get("file")
    fileid = ""
    if file is not None:
        fileid = str(random.randint(11111111,999999999)) + file.name
        filename = os.path.join(settings.MEDIA_ROOT,"editor_images", fileid)
        # print(settings.MEDIA_URL + filename.replace(str(settings.BASE_DIR), '').replace("/media",""))  
        with open(filename, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        return HttpResponse(settings.MEDIA_URL + filename.replace(str(settings.BASE_DIR), '').replace("/media",""))  
    else:
        return HttpResponse("Failed to upload file")