import sqlite3 as sql

DB_NAME = "Dimitris.db"

def init():
    database = sql.connect(DB_NAME)

    cursor = database.cursor()
    
    # ========
    # Products
    # ========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        productId INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        type TEXT,
        description TEXT,
        price REAL,
        brand TEXT,
        image TEXT,
        quantity INTEGER DEFAULT 0
    )'''
    )

    # ==================
    # Customers Reviews
    # ==================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        comment TEXT NOT NULL,
        FOREIGN KEY(product_id) REFERENCES Products(id)
    )'''
    )

    database.commit()

def add_product(title, type, description, price, brand, image, quantity):
    connection = sql.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Products (title, type, description, price, brand, image, quantity)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, type, description, price, brand, image, quantity))

    connection.commit()
    connection.close()
    print(f"Added product: {title}")

def add_comment(product_id, comment):
    connection = sql.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO Reviews (product_id, comment)
        VALUES (?, ?)
    ''', (product_id, comment))

    connection.commit()
    connection.close()
    print(f"Added comment: {comment}")


init()

add_product("MacBook Air M3", "LAPTOP", "cpu: Apple M3 Chip ram: 8GB Unified storage: 256GB SSD screen: 13.6 Liquid Retina battery: 18 Hours", 1249, "APPLE", "https://www.notebookcheck.net/fileadmin/Notebooks/Apple/MacBook_Air_13_M3_10C_GPU/IMG_2758.JPG", 9)
add_product("HP Omen 16", "LAPTOP", "cpu: Intel Core i7-13700H gpu: NVIDIA RTX 4060 ram: 16GB DDR5 storage: 512GB NVMe screen: 16.1 FHD 144Hz", 1499, "HP", "https://a.scdn.gr/images/sku_main_images/043990/43990797/xlarge_20250702144152_hp_omen_16_xf0003nv_16_1_ips_fhd_165hz_ryzen_7_7840hs_16gb_1tb_ssd_geforce_rtx_4070_w11_home_black_gr_keyboard.jpeg", 16)
add_product("Legion Pro 5", "LAPTOP", "cpu: AMD Ryzen 7 7745HX gpu: NVIDIA RTX 4070 ram: 32GB DDR5 storage: 1TB SSD screen: 16 WQHD+ 240Hz", 1699, "LENOVO", "https://a.scdn.gr/images/sku_main_images/050547/50547742/xlarge_20240216100731_lenovo_legion_pro_5_16irx9_16_ips_165hz_i9_14900hx_32gb_1tb_ssd_geforce_rtx_4070_onyx_grey_gr_keyboard.jpeg", 4)
add_product("XPS 13 Plus", "LAPTOP", "cpu: Intel Core i7-1360P ram: 16GB LPDDR5 storage: 512GB SSD screen: 13.4 OLED 3.5K feature: Touch Bar", 1899, "DELL", "https://a.scdn.gr/images/sku_images/061473/61473255/20220622163127_f85e7479.jpeg", 35)
add_product("ROG Zephyrus G14", "LAPTOP", "cpu: AMD Ryzen 9 7940HS gpu: RTX 4060 ram: 16GB storage: 1TB NVMe screen: 14 Nebula HDR", 1999, "ASUS", "https://dlcdnwebimgs.asus.com/gain/BA146EC2-FF9D-4A8E-A91A-C9F864DE6BBB", 54)
add_product("Surface Laptop 5", "LAPTOP", "cpu: Intel Evo i5 ram: 8GB storage: 256GB screen: 13.5 PixelSense feature: Touchscreen", 1199, "MICROSOFT", "https://i.ytimg.com/vi/9_FQW36r0n8/maxresdefault.jpg", 66)
add_product("Galaxy S24 Ultra", "PHONE", "cpu: Snapdragon 8 Gen 3 ram: 12GB storage: 256GB camera: 200MP Main battery: 5000mAh feature: S-Pen", 1449, "SAMSUNG", "https://bbpcdn.pstatic.gr/bpimg3/9Ra2T/1TofLw_SX340/1734611790/samsung-galaxy-s24-ultra-256gb.webp", 97)
add_product("iPhone 15 Pro Max", "PHONE", "cpu: A17 Pro ram: 8GB storage: 256GB camera: 48MP / 5x Zoom battery: 4422mAh feature: Titanium Body", 1499, "APPLE", "https://smartbee.gr/image/cache/catalog/%CE%A0%CE%A1%CE%9F%CE%99%CE%9F%CE%9D%CE%A4%CE%91/19-550x550h.jpeg", 59)
add_product("Pixel 8 Pro", "PHONE", "cpu: Google Tensor G3 ram: 12GB storage: 128GB camera: 50MP AI battery: 5050mAh feature: Magic Editor", 1099, "GOOGLE", "https://cdn.lagonika.gr/uploads/offers/2024/07/7170fm_WL_9_EL_AC_SL_1500_b4463d49e8.jpg", 83)
add_product("Xiaomi 14 Ultra", "PHONE", "cpu: Snapdragon 8 Gen 3 ram: 16GB storage: 512GB camera: Leica Quad Lens battery: 5000mAh feature: 90W Charging", 1399, "XIAOMI", "https://i02.appmifile.com/91_operatorx_operatorx_opx/24/02/2024/4eafcd40186edde466860564f9ff71e9.png", 30)
add_product("OnePlus 12", "PHONE", "cpu: Snapdragon 8 Gen 3 ram: 16GB storage: 512GB camera: Hasselblad battery: 5400mAh feature: 100W Charging", 949, "ONEPLUS", "https://oasis.opstatics.com/content/dam/oasis/page/2023/cn/12/12-green.png", 6)
add_product("Galaxy A55 5G", "PHONE", "cpu: Exynos 1480 ram: 8GB storage: 128GB camera: 50MP battery: 5000mAh screen: Super AMOLED", 499, "SAMSUNG", "https://cdn-files.kimovil.com/default/0009/97/thumb_896036_default_big.jpg", 44)
add_product("WH-1000XM5", "AUDIO", "category: Over-Ear anc: Κορυφαίο battery: 30 Hours connection: Bluetooth 5.2 feature: Multipoint", 399, "SONY", "https://m.media-amazon.com/images/I/61BGLYEN-xL._AC_UF894,1000_QL80_.jpg", 88)
add_product("QC Ultra", "AUDIO", "category: Over-Ear anc: CustomTune battery: 24 Hours connection: Bluetooth 5.3 feature: Immersive Audio", 399, "BOSE", "https://audiogroup.com.gr/cdn/shop/files/CREA-1001_QCUH24_White_ThreeQuarter_Left_PhoneComp_x2a_RGB.jpg?v=1726080826", 21)
add_product("AirPods Pro 2", "AUDIO", "category: In-Ear anc: 2x Καλύτερο battery: 6+30 Hours connection: Bluetooth 5.3 feature: H2 Chip", 249, "APPLE", "https://c.scdn.gr/ds/c2c/item_images/h-RY01n82jFr/thumbnail_20260103040127_92cdaa91.jpeg", 85)
add_product("Flip 6", "AUDIO", "category: Ηχείο power: 20W RMS battery: 12 Hours feature: Αδιάβροχο IP67 connection: Bluetooth 5.1", 119, "JBL", "https://d.scdn.gr/images/sku_main_images/031085/31085273/xlarge_20210920101722_jbl_flip_6_adiavrocho_icheio_bluetooth_me_12_ores_leitourgias_black.jpeg", 76)
add_product("Major IV", "AUDIO", "category: On-Ear battery: 80+ Hours connection: Bluetooth 5.0 feature: Ασύρματη Φόρτιση design: Retro", 149, "MARSHALL", "https://assets.egalaxy.gr/media/catalog/product/cache/b2d63a3599e7f10a16c1d8d02b7a556e/1/0/1005773_1.jpg", 68)
add_product("Momentum TW 3", "AUDIO", "category: In-Ear anc: Adaptive battery: 28 Hours connection: aptX Adaptive feature: High-Res Audio", 299, "SENNHEISER", "https://m.media-amazon.com/images/I/6165ykR16dL.jpg", 25)
add_product("Sonos Roam", "AUDIO", "category: Φορητό Ηχείο power: WiFi & Bluetooth battery: 10 Hours feature: Αδιάβροχο IP67 connection: AirPlay 2", 179, "SONOS", "https://www.germanos.gr/images/category6/20433290/20433290_BluetoothSONOSRoam2_medium_0.png", 52)
add_product("Wonderboom 3", "AUDIO", "category: Ηχείο 360° power: Outdoor Mode battery: 14 Hours feature: Επιπλέει στο νερό connection: Bluetooth", 99, "ULTIMATE EARS", "https://c.scdn.gr/images/sku_main_images/039812/39812705/xlarge_20221201180537_logitech_wonderboom_3_984_001829_icheio_bluetooth_8_5w_me_diarkeia_mpatarias_eos_14_ores_mayro.jpeg", 46)
add_product("Galaxy Buds2 Pro", "AUDIO", "category: In-Ear anc: Intelligent ANC battery: 5+18 Hours connection: Bluetooth 5.3 feature: 24-bit Hi-Fi", 169, "SAMSUNG", "https://www.zdnet.com/a/img/resize/cb0c294086b6e74591369135f7dc061c7fa3926e/2022/08/12/50f0ef5f-885c-4449-a633-992f70ba7c67/galaxy-buds-2-pro-2.jpg?auto=webp&fit=crop&height=1200&width=1200", 54)
add_product("Nothing Ear (2)", "AUDIO", "category: In-Ear anc: Personalized battery: 36 Hours (θήκη) connection: LHDC 5.0 design: Διάφανο", 149, "NOTHING", "https://b.scdn.gr/images/sku_main_images/044721/44721754/xlarge_20230727110444_nothing_ear_2_in_ear_bluetooth_handsfree_akoustika_me_antochi_ston_idrota_kai_thiki_fortisis_mayra.jpeg", 86)
add_product("Beats Studio Pro", "AUDIO", "category: Over-Ear anc: Fully Adaptive battery: 40 Hours connection: USB-C Lossless feature: Spatial Audio", 399, "BEATS", "https://m.media-amazon.com/images/I/61u-OaDSfQL._AC_UF894,1000_QL80_.jpg", 99)
add_product("Px7 S2e", "AUDIO", "category: Over-Ear anc: Υβριδικό battery: 30 Hours connection: aptX Adaptive design: Premium Υλικά", 429, "BOWERS & WILKINS", "https://static1.apothema.gr/files/productImages/s/bowers-wilkins-px7-s2e-asyrmata-bluetooth-over-ear-akoustika-me-30-ores-leitourgias-mayra-14-fp44520-6440551.jpg", 78)
add_product("RTX 4060 8GB", "GPU", "memory: 8GB GDDR6 ports: HDMI, 3x DP power: 115W TDP feature: DLSS 3.0", 329, "NVIDIA", "https://d.scdn.gr/images/sku_main_images/043711/43711724/20230630094808_gigabyte_geforce_rtx_4060_8gb_gddr6_eagle_oc_karta_grafikon_gv_n4060eagle_oc_8gd.jpeg", 73)
add_product("RTX 4070 12GB", "GPU", "memory: 12GB GDDR6X ports: HDMI, 3x DP power: 200W TDP feature: Ray Tracing", 599, "NVIDIA", "https://www.e-shop.gr/images/PER/BIG/PER.607402.jpg", 19)   
add_product("Radeon RX 7800 XT", "GPU", "memory: 16GB GDDR6 ports: HDMI 2.1, DP 2.1 power: 263W TDP feature: FSR 3", 549, "AMD", "https://www.e-shop.gr/images/PER/BIG/PER.232261.jpg", 49)    
add_product("Ryzen 5 5600X", "CPU", "cores: 6 Cores / 12 Threads socket: AM4 clock: Up to 4.6GHz cooler: Wraith Stealth", 199, "AMD", "https://www.amd.com/content/dam/amd/en/images/products/processors/ryzen/2505503-ryzen-5-5600x.jpg", 75)
add_product("Ryzen 7 5800X", "CPU", "cores: 8 Cores / 16 Threads socket: AM4 clock: Up to 4.7GHz tdp: 105W", 299, "AMD", "https://www.e-active.gr/pub/media/catalog/product/cache/e3737e95c44d4fd25a472509b026ccfa/a/m/amd-ryzen-7-5800x-box.jpg", 71)
add_product("Core i5-12600K", "CPU", "cores: 10 Cores (6P+4E) socket: LGA 1700 clock: Up to 4.9GHz graphics: UHD 770", 269, "INTEL", "https://cdn.panacompu.com/cdn-img/pv/intel-core-i5-12600k-box-and-chipset-back.jpg?width=550&height=400&fixedwidthheight=false", 6)
add_product("Core i7-12700K", "CPU", "cores: 12 Cores (8P+4E) socket: LGA 1700 clock: Up to 5.0GHz graphics: UHD 770", 399, "INTEL", "https://i.pcmag.com/imagery/reviews/07rfvBq3YYV4bfaooOD3INP-4.fit_lim.size_1050x.jpg", 81)
add_product("Vengeance 16GB DDR4", "RAM", "capacity: 16GB (2x8GB) speed: 3200MHz cas: CL16 profile: Low Profile", 79, "CORSAIR", "https://a.scdn.gr/images/sku_images/051664/51664632/20211102145207_ff0d8484.jpeg", 66)
add_product("Trident Z Neo 32GB DDR4", "RAM", "capacity: 32GB (2x16GB) speed: 3600MHz cas: CL16 feature: RGB Sync", 149, "G.SKILL", "https://www.tradeinn.com/f/13806/138060577/g.skill-trident-z-neo-32gb-2x16gb-ddr4-3600mhz-rgb-ram.webp", 24)
add_product("970 EVO Plus 1TB", "STORAGE", "category: M.2 NVMe interface: PCIe 3.0 read: 3500 MB/s write: 3300 MB/s", 89, "SAMSUNG", "https://gfx3.senetic.com/akeneo-catalog/f/8/a/1/f8a1845c5d351be6d36ab5574ee5263428b72a99_1045206_MZ_V7S1T0BW_image7.jpg", 41)
add_product("WD Blue 2TB SSD", "STORAGE", "category: 2.5 SATA capacity: 2TB read: 560 MB/s write: 530 MB/s", 119, "WESTERN DIGITAL", "https://www.priveshop.gr/public/img/products/75476_20240130132350.jpeg", 91)
add_product("UltraGear 27GL850", "MONITOR", "screen: 27 Nano IPS resolution: 2560 x 1440 hz: 144Hz response: 1ms", 399, "LG", "https://assets.kotsovolos.gr/product/222040-b.jpg", 33)
add_product("Odyssey G5 32", "MONITOR", "screen: 32 VA Curved resolution: 2560 x 1440 hz: 144Hz curve: 1000R", 349, "SAMSUNG", "https://images.samsung.com/is/image/samsung/p6pim/za/ls32cg552euxen/gallery/za-odyssey-g5-32g55c-496255-ls32cg552euxen-547857001?$Q90_1248_936_F_PNG$", 84)
add_product("K70 RGB MK.2", "KEYBOARD", "category: Mechanical switches: Cherry MX Red frame: Aluminum feature: Wrist Rest", 129, "CORSAIR", "https://ggalaxy.gr/media/catalog/product/cache/0cc6d5d0cb45d44e6222ecf5ecf5655f/c/o/corsair-k70-rgb-mk2-low-profile-rapidfire-mechanical-gaming-keyboard-gr-1-mini.jpg", 19)
add_product("G513 Carbon", "KEYBOARD", "category: Mechanical switches: GX Brown (Tactile) frame: Carbon Alloy feature: Memory Foam Rest", 119, "LOGITECH", "https://cdn.ozon.gr/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/g/e/983dde98766bf67f3aa56dc19321618b/mixaniko-pliktrologio-logitech---g513-carbon--gx-brown--rgb--mauro-30.jpg", 92)
add_product("G502 HERO", "MICE", "sensor: HERO 25K dpi: 25.600 buttons: 11 Programmable weight: Adjustable", 59, "LOGITECH", "https://www.logitechg.com/content/dam/gaming/en/non-braid/hyjal-g502-hero/2025/g502-hero-mouse-top-angle-gallery-1.png", 85)
add_product("DeathAdder V2", "MICE", "sensor: Focus+ dpi: 20.000 switches: Optical weight: 82g", 69, "RAZER", "https://assets.razerzone.com/eeimages/support/products/1612/1612_razerdeathadderv2.png", 9)
add_product("Cloud II", "AUDIO", "category: Over-Ear connection: Wired (USB/3.5mm) sound: 7.1 Surround mic: Detachable", 99, "HYPERX", "https://b.scdn.gr/images/sku_main_images/020312/20312949/xlarge_20190930124525_hyperx_cloud_ii_red.jpeg", 71)
add_product("iPhone 14", "PHONE", "cpu: A15 Bionic ram: 6GB storage: 128GB camera: 12MP Dual battery: 3279mAh", 799, "APPLE", "https://bbpcdn.pstatic.gr/bpimg36/76mBm/1SYzV1_SX340/1728492731/apple-iphone-14-128gb.webp", 64)
add_product("Galaxy S23", "PHONE", "cpu: Snapdragon 8 Gen 2 ram: 8GB storage: 256GB camera: 50MP (main) battery: 3900mAh", 749, "SAMSUNG", "https://cdn.shopflix.gr/products/SFA-08179961/images/530/images_by_date_2023_August_smartphones_fix_import_SF_08179961.jpeg", 36)
add_product("Pixel 7", "PHONE", "cpu: Tensor G2 ram: 8GB storage: 128GB camera: 50MP + 12MP battery: 4355mAh", 599, "GOOGLE", "https://d2e6ccujb3mkqf.cloudfront.net/35fef6fb-df24-484b-b4d0-95b235303cf2.jpg", 71)
add_product("Vengeance Kraken-V79 Gaming Desktop PC", "PC", "cpu: 'AMD Ryzen 9-7900' ram: '32GB DDR5' storage: 'SSD 1TB' gpu: 'RΤX 5060 8GB' rgb: 'yes'", 1499, "-", "https://d.scdn.gr/images/sku_main_images/060343/60343397/xlarge_20250512112156_vengeance_kraken_v79_gaming_desktop_pc_ryzen_9_7900_32gb_ddr5_1tb_ssd_no_os.jpeg", 45)
add_product("Phantom X Budget Gaming PC", "PC", "cpu: 'Ryzen 5 5600' ram: '16GB DDR4' storage: '1TB SSD' gpu: 'RTX 3060 12GB' rgb: 'Yes'", 999, "-", "https://a.scdn.gr/images/sku_main_images/037217/37217571/xlarge_20220719120212_vengeance_phantom_x_gaming_desktop_pc_ryzen_5_5500_16gb_ddr4_512gb_ssd_geforce_gtx_1650_no_os.jpeg", 23)
add_product("Nova Creator Workstation PC", "PC", "cpu: 'Ryzen 9 7950X' ram: '64GB DDR5' storage: '4TB NVMe' gpu: 'RTX 4090 24GB' rgb: 'Minimal'", 3299, "-", "https://a.scdn.gr/images/sku_main_images/064514/64514063/xlarge_20251204162735_nova_nova_series_desktop_pc_ryzen_7_8700g_32gb_ddr5_1tb_ssd_no_os.jpeg", 10)
add_product("Stealth Office Pro Desktop", "PC", "cpu: 'Intel Core i5-12400' ram: '16GB DDR4' storage: '512GB SSD' gpu: 'Integrated UHD 730' rgb: 'No'", 799, "-", "https://bbpcdn.pstatic.gr/bpimg3/2mpOEP/1VI9bE_SX660/1768905734/i-abox-office-value-v2.webp", 100)